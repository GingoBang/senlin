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


class TestReceiverCreate(base.BaseSenlinTest):

    @classmethod
    def resource_setup(cls):
        super(TestReceiverCreate, cls).resource_setup()
        # Create profile
        cls.profile = cls.create_profile(constants.spec_nova_server)
        # Create a test cluster
        cls.cluster = cls.create_test_cluster(cls.profile['id'],
                                              0, min_size=0, max_size=-1)
        cls.receivers = []

    @classmethod
    def resource_cleanup(cls):
        # Delete receivers
        for recv in cls.receivers:
            cls.delete_receiver(recv)
        # Delete test cluster
        cls.delete_test_cluster(cls.cluster['id'])
        # Delete profile
        cls.delete_profile(cls.profile['id'])
        super(TestReceiverCreate, cls).resource_cleanup()

    @decorators.idempotent_id('55f06733-af40-4fa8-a1de-3cb2a0c700d7')
    def test_create_receiver(self):
        params = {
            'receiver': {
                'name': 'test-receiver',
                'cluster_id': self.cluster['id'],
                'type': 'webhook',
                'action': 'CLUSTER_SCALE_IN',
                'params': {"count": 5}
            }
        }
        res = self.client.create_obj('receivers', params)

        # Verify resp of receiver create API
        self.assertEqual(201, res['status'])
        self.assertIsNotNone(res['body'])
        recv = res['body']
        self.receivers.append(recv['id'])
        for key in ['action', 'actor', 'channel', 'cluster_id', 'created_at',
                    'domain', 'id', 'name', 'params', 'project', 'type',
                    'updated_at', 'user']:
            self.assertIn(key, recv)
        self.assertEqual('test-receiver', recv['name'])
        self.assertEqual(self.cluster['id'], recv['cluster_id'])
        self.assertEqual('webhook', recv['type'])
        self.assertEqual({"count": 5}, recv['params'])
