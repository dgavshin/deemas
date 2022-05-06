from server.app import ma
from server.app.models import Service, ScriptRule, ConditionRule


class ConditionRuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ConditionRule
        include_relationships = True
        include_fk = True
        load_instance = True


class ScriptRuleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScriptRule
        include_relationships = True
        include_fk = True
        load_instance = True


class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        include_relationships = True
        load_instance = True
    name = ma.String(required=False)
    condition_rules = ma.Nested(ConditionRuleSchema(many=True), many=True, exclude=("service",))
    script_rules = ma.Nested(ScriptRuleSchema(many=True), many=True, exclude=("service",))
