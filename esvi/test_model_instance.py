import unittest

try:
    from esvi.model_instance import ModelInstance
    import esvi.fields
except:
    from model_instance import ModelInstance
    import fields

class TestModelInstance(unittest.TestCase):
    def _create_instance(self):
        model_fields = {'age': fields.IntegerField(),
                        'name': fields.StringField(),
                        'number': fields.StringField()}

        model_content = {'age':5, 'name':"Jack", 'number':"12345678"}

        instance = ModelInstance(model_name="Contact",
                                 model_fields=model_fields,
                                 model_content=model_content)

        return instance


    def test_class_name(self):
        instance = self._create_instance()
        expected_class_name = "Contact_instance"

        actual_class_name = instance.__class__.__name__

        self.assertEqual(expected_class_name, actual_class_name)

    def test_get_valid_field(self):
        instance = self._create_instance()
        expected_age_value = 5
        actual_age_value = instance.get('age')
        self.assertEqual(expected_age_value, actual_age_value)

    def test_get_invalid_field(self):
        instance = self._create_instance()
        with self.assertRaises(Exception):
            instance.get('height')

    def test_set_valid_field(self):
        instance = self._create_instance()
        value_to_set = "Johnny"

        instance.set('name', value_to_set)
        value_set_in_class = instance.content['name']

        self.assertEqual(value_to_set, value_set_in_class)

    def test_set_invalid_field(self):
        instance = self._create_instance()
        with self.assertRaises(Exception):
            instance.set('height')

    def test_staged_changes(self):
        instance = self._create_instance()
        instance.set('name', "Walker")
        instance.set('age', 29)

        staged_changes = instance._staged_changes

        self.assertTrue('name' in staged_changes and 'age' in staged_changes)

        self.assertEqual(instance.get('name'), "Walker")
        self.assertEqual(instance.get('age'), 29)

if __name__=='__main__':
    unittest.main()
