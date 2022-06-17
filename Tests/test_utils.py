import unittest
from unittest import TestCase, mock
from unittest.mock import patch
import GUI.utils

########################################################################################################################
# File for testing the utils.py file.
########################################################################################################################

class TestUtils(TestCase):

    @mock.patch("GUI.utils.pd")
    @mock.patch("GUI.utils.get_blood_test_values")
    def test_make_prediction(self, mock_pd, mock_get_blood):
        with patch('GUI.utils.find_prediction') as mock_find:
            mock_pd.read_excel().to_numpy().return_value = mock.MagicMock()
            mock_get_blood.return_value = ["WBC", "LYMF", "GRAN", "MID", "RBC", "HGB", "MCH", "MCHC", "MPV", "PLT"]
            test_path = ""
            test_model = mock.Mock()
            test_list = []
            mock_find.return_value = [1, 1]
            GUI.utils.make_prediction(test_path, 0, test_model, test_list)
            mock_find.assert_called_once()
            mock_pd.read_excel().to_numpy.assert_called_once()

    def test_find_prediction(self):
        test_data = [1, 1]
        test_model = mock.Mock()
        test_model.predict.return_value = 1
        self.assertEqual(1, GUI.utils.find_prediction(test_data, test_model, 0)[1])

    @mock.patch("GUI.utils.QMessageBox")
    def test_pop_message_box(self, mock_message):
        GUI.utils.pop_message_box("Hello")
        mock_message.assert_called_once()

    def test_get_seal_species_str_from_int(self):
        self.assertEqual("Phoca Vitulina", GUI.utils.get_seal_species_str_from_int(0))
        self.assertEqual("Halichoerus Grypus", GUI.utils.get_seal_species_str_from_int(1))

    def test_get_sex_str_from_int(self):
        self.assertEqual("Female", GUI.utils.get_sex_str_from_int(0))
        self.assertEqual("Male", GUI.utils.get_sex_str_from_int(1))

    def test_get_chances_str_from_int(self):
        self.assertEqual("Will not survive", GUI.utils.get_chances_str_from_int(0))
        self.assertEqual("Will survive", GUI.utils.get_chances_str_from_int(1))

    def test_get_seal_species_int(self):
        self.assertEqual(0, GUI.utils.get_seal_species_int("Phoca Vitulina"))
        self.assertEqual(1, GUI.utils.get_seal_species_int("Halichoerus Grypus"))

    def test_get_sex_int(self):
        self.assertEqual(0, GUI.utils.get_sex_int("Female"))
        self.assertEqual(1, GUI.utils.get_sex_int("Male"))

    def test_get_survival_str_from_int(self):
        self.assertEqual("Not released", GUI.utils.get_survival_str_from_int(0))
        self.assertEqual("Released", GUI.utils.get_survival_str_from_int(1))


if __name__ == '__main__':
    unittest.main()


