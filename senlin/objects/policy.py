# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Policy object."""

from oslo_versionedobjects import base
from oslo_versionedobjects import fields

from senlin.db import api as db_api
from senlin.objects import base as senlin_base


class Policy(senlin_base.SenlinObject, base.VersionedObjectDictCompat):
    """Senlin policy object."""

    fields = {
        'id': fields.UUIDField(),
        'name': fields.StringField(),
        'type': fields.StringField(),
        'spec': fields.DictOfStringsField(),
        'cooldown': fields.IntegerField(nullable=True),
        'level': fields.IntegerField(nullable=True),
        'data': fields.DictOfStringsField(),
        'created_at': fields.DateTimeField(),
        'updated_at': fields.DateTimeField(),
        'user': fields.StringField(),
        'project': fields.StringField(),
        'domain': fields.StringField(nullable=True),
    }

    @staticmethod
    def _from_db_object(context, policy, db_obj):
        if db_obj is None:
            return None

        for field in policy.fields:
            policy[field] = db_obj[field]

        policy._context = context
        policy.obj_reset_changes()

        return policy

    @classmethod
    def create(cls, context, values):
        obj = db_api.policy_create(context, values)
        return cls._from_db_object(context, cls(context), obj)

    @classmethod
    def get(cls, context, policy_id, **kwargs):
        obj = db_api.policy_get(context, policy_id, **kwargs)
        return cls._from_db_object(context, cls(), obj)

    @classmethod
    def get_by_name(cls, context, name, **kwargs):
        obj = db_api.policy_get_by_name(context, name, **kwargs)
        return cls._from_db_object(context, cls(), obj)

    @classmethod
    def get_by_short_id(cls, context, short_id, **kwargs):
        obj = db_api.policy_get_by_short_id(context, short_id, **kwargs)
        return cls._from_db_object(context, cls(), obj)

    @classmethod
    def get_all(cls, context, **kwargs):
        objs = db_api.policy_get_all(context, **kwargs)
        return [cls._from_db_object(context, cls(), obj) for obj in objs]

    @classmethod
    def update(cls, context, obj_id, values):
        obj = db_api.policy_update(context, obj_id, values)
        return cls._from_db_object(context, cls(), obj)

    @classmethod
    def delete(cls, context, obj_id):
        db_api.policy_delete(context, obj_id)
