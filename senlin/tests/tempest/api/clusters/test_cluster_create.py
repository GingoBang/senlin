# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from tempest.lib import decorators

from senlin.tests.tempest.api import base
from senlin.tests.tempest.common import constants


class TestClusterCreate(base.BaseSenlinTest):

    @classmethod
    def resource_setup(cls):
        super(TestClusterCreate, cls).resource_setup()
        # Create profile
        cls.profile = cls.create_profile(
            constants.spec_nova_server)

    @classmethod
    def resource_cleanup(cls):
        # Delete profile
        cls.delete_profile(cls.profile['id'])
        super(TestClusterCreate, cls).resource_cleanup()

    @decorators.idempotent_id('61cbe340-937a-40d5-9d2f-067f2c7cafcc')
    def test_cluster_create_all_attrs_defined(self):
        # Create cluster
        name = 'test-cluster'
        desired_capacity = 2
        min_size = 1
        max_size = 3
        metadata = {'k1': 'v1'}
        timeout = 120
        params = {
            'cluster': {
                'profile_id': self.profile['id'],
                'desired_capacity': desired_capacity,
                'min_size': min_size,
                'max_size': max_size,
                'timeout': timeout,
                'metadata': {'k1': 'v1'},
                'name': 'test-cluster'
            }
        }
        res = self.client.create_obj('clusters', params)

        # Verify resp of cluster create API
        self.assertEqual(202, res['status'])
        self.assertIsNotNone(res['body'])
        self.assertIn('actions', res['location'])
        cluster = res['body']
        for key in ['created_at', 'data', 'domain', 'id', 'init_at', 'nodes',
                    'policies', 'profile_id', 'profile_name', 'project',
                    'status', 'status_reason', 'updated_at', 'user']:
            self.assertIn(key, cluster)
        self.assertIn(name, cluster['name'])
        self.assertEqual(desired_capacity, cluster['desired_capacity'])
        self.assertEqual(min_size, cluster['min_size'])
        self.assertEqual(max_size, cluster['max_size'])
        self.assertEqual(metadata, cluster['metadata'])
        self.assertEqual(timeout, cluster['timeout'])

        def cleanup_cluster():
            self.delete_test_cluster(cluster['id'])

        self.addCleanup(cleanup_cluster)

        # Wait cluster to be active before moving on
        action_id = res['location'].split('/actions/')[1]
        self.wait_for_status('actions', action_id, 'SUCCEEDED')
