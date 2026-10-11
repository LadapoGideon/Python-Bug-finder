import unittest

from bug_finder import find_issues


class BugFinderTests(unittest.TestCase):
    def test_mutable_default_is_flagged(self):
        issues = find_issues("def add_item(item, items=[]):\n    items.append(item)\n    return items")
        self.assertEqual(issues, [(1, "mutable default argument in 'add_item'")])

    def test_bare_except_is_flagged(self):
        source = "try:\n    x = 1\nexcept:\n    pass"
        messages = [m for _, m in find_issues(source)]
        self.assertTrue(any("bare 'except:'" in m for m in messages))

    def test_equality_with_none_is_flagged(self):
        issues = find_issues("if value == None:\n    pass")
        self.assertEqual(len(issues), 1)
        self.assertIn("is None", issues[0][1].replace("'is' or 'is not'", "is None"))

    def test_clean_code_has_no_issues(self):
        source = "def greet(name=None):\n    if name is None:\n        return 'hi'\n    return f'hi {name}'"
        self.assertEqual(find_issues(source), [])

    def test_eval_is_flagged(self):
        issues = find_issues("result = eval(user_input)")
        self.assertEqual(len(issues), 1)
        self.assertIn("eval()", issues[0][1])


if __name__ == "__main__":
    unittest.main()
