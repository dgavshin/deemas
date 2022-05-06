from unittest import TestCase, main

import test_helper
from server import load_rules, RuleType, RuleProtocol, LoadRulesRequest, config


class TestRulesLoading(TestCase):

    def test_load_valid_rule(self):
        config.RULE_PATH = "./valid_rules"
        try:
            rules = load_rules(LoadRulesRequest(RuleProtocol.HTTP, RuleType.ENCRYPT))
            self.assertEqual(len(rules), 1)
            self.assertEqual(rules[0].check(None), True)
        except ValueError:
            self.fail("Загрузка валидных правил прервалась исключением")

    def test_load_rule_without_check_function(self):
        config.RULE_PATH = "./invalid_rules"
        load_rules(LoadRulesRequest(RuleProtocol.HTTP, RuleType.ENCRYPT, "no_check_function"))
        self.assertRegex(test_helper.last_logged_message, "нет метода check")

    def test_load_rule_with_invalid_return_type(self):
        config.RULE_PATH = "./invalid_rules"
        load_rules(LoadRulesRequest(RuleProtocol.HTTP, RuleType.ENCRYPT, service_name="invalid_return_type"))
        self.assertRegex(test_helper.last_logged_message, "тип возвращаемого значения не")

    def test_load_rule_with_invalid_parameter_type(self):
        config.RULE_PATH = "./invalid_rules"
        load_rules(LoadRulesRequest(RuleProtocol.HTTP, RuleType.DECRYPT, service_name="invalid_parameter_type"))
        self.assertRegex(test_helper.last_logged_message, "тип параметра не")

    def test_do_not_load_rules(self):
        config.RULE_PATH = "./invalid_rules"
        modules = load_rules(LoadRulesRequest(RuleProtocol.HTTP, RuleType.DECRYPT, service_name="no_valid_filenames"))
        self.assertEqual(len(modules), 0)

    def test_banned_rules(self):
        config.RULE_PATH = "./valid_rules"
        loaded = load_rules(LoadRulesRequest(RuleProtocol.HTTP, RuleType.DECRYPT, banned_rules="example"))
        self.assertTrue(len(loaded) == 0)

    def test_specified_rules_by_service_name(self):
        config.RULE_PATH = "./valid_rules"
        loaded = load_rules(LoadRulesRequest(
            RuleProtocol.HTTP,
            RuleType.DECRYPT,
            service_name="service")
        )
        self.assertEqual(1, len(loaded))


if __name__ == '__main__':

    main()
