#!/usr/bin/python

import unittest
from solution import percolate


class OutputFormatTests(unittest.TestCase):
  def testGivenInputGivesExpectedOutput(self):
    sample_data = [
      'Booker T., Washington, 87360, 373 781 7380, yellow',
      'Chandler, Kerri, (623)-668-9293, pink, 123123121',
      'James Murphy, yellow, 83880, 018 154 6474',
      'asdfawefawea',
    ]

    percolate_expected_output = {
      "entries": [
      {
        "color": "yellow", 
        "firstname": "James", 
        "lastname": "Murphy", 
        "phonenumber": "018-154-6474", 
        "zipcode": "83880"
      }, 
      {
        "color": "yellow", 
        "firstname": "Booker T.", 
        "lastname": "Washington", 
        "phonenumber": "373-781-7380", 
        "zipcode": "87360"
      }
      ], 
      "errors": [
        1, 
        3
      ]
    }

    result = percolate.parse_data(sample_data)
    self.assertEquals(result, percolate_expected_output)


class FormatParserTests(unittest.TestCase):
  def setUp(self):
    self.test_data = 'Booker T., Washington, 87360, 373 781 7380, yellow'

  def testFormatPhoneNumber(self):
    format_parser = percolate.FormatParser(self.test_data)

    valid_number1 = "373-781-7380"
    valid_number2 = "(623)-668-9293"
    valid_number3 = "3737817380"
    valid_number4 = "454 934 6454"
    invalid_number = "11111111111"

    self.assertEquals(format_parser.FormatPhoneNumber(valid_number1),
                      '373-781-7380')
    self.assertEquals(format_parser.FormatPhoneNumber(valid_number2),
                      '623-668-9293')
    self.assertEquals(format_parser.FormatPhoneNumber(valid_number3),
                      '373-781-7380')
    self.assertEquals(format_parser.FormatPhoneNumber(valid_number4),
                      '454-934-6454')
    self.assertFalse(format_parser.FormatPhoneNumber(invalid_number))

  def testIsValidZipcode(self):
    format_parser = percolate.FormatParser(self.test_data)

    valid_zipcode = '10003'
    invalid_zipcode1 = '12345678'
    invalid_zipcode2 = 'abcde'

    self.assertTrue(format_parser.IsValidZipcode(valid_zipcode))
    self.assertFalse(format_parser.IsValidZipcode(invalid_zipcode1))
    self.assertFalse(format_parser.IsValidZipcode(invalid_zipcode2))


class FormatParser1Tests(unittest.TestCase):
  def testFormatParser(self):
    inputted = 'Zlotnik, Zack, 123-456-7890, Blue, 12345'
    expected = {
      "color": "Blue",
      "firstname": "Zack",
      "lastname": "Zlotnik",
      "phonenumber": "123-456-7890",
      "zipcode": "12345"
    }

    format_parser = percolate.FormatParser1(inputted)
    self.assertEquals(format_parser.GetFormattedData(), expected)

  def testInvalidFormats(self):
    invalid_data = [
      'James Murphy, yellow, 83880, 018 154 6474',
      'Booker T., Washington, 87360, 373 781 7380, yellow',
      'Chandler, Kerri, (623)-668-9293, pink, 123123121',
      'asdfawefawea' 
    ]

    for item in invalid_data:
      parsed_data = percolate.FormatParser1(item).GetFormattedData()
      self.assertFalse(parsed_data)


class FormatParser2Tests(unittest.TestCase):
  def testFormatParser(self):
    inputted = 'James Murphy, yellow, 83880, 018 154 6474'
    expected = {
      "color": "yellow",
      "firstname": "James",
      "lastname": "Murphy",
      "phonenumber": "018-154-6474",
      "zipcode": "83880"
    }

    format_parser = percolate.FormatParser2(inputted)
    self.assertEquals(format_parser.GetFormattedData(), expected)

  def testFormatParser_MiddleInitial(self):
    inputted = 'Englebert G. Humperdink, red, 36410, 839 014 8051'
    expected = {
      "color": "red",
      "firstname": "Englebert G.",
      "lastname": "Humperdink",
      "zipcode": "36410",
      "phonenumber": "839-014-8051"
    }

    format_parser = percolate.FormatParser2(inputted)
    self.assertEquals(format_parser.GetFormattedData(), expected)

  def testInvalidFormats(self):
    invalid_data = [
      'Zlotnik, Zack, 123-456-7890, Blue, 12345',
      'Booker T., Washington, 87360, 373 781 7380, yellow'
      'Chandler, Kerri, (623)-668-9293, pink, 123123121',
      'asdfawefawea' 
    ]

    for item in invalid_data:
      parsed_data = percolate.FormatParser2(item).GetFormattedData()
      self.assertFalse(parsed_data)

class FormatParser3Tests(unittest.TestCase):
  def testFormatParser(self):
    inputted = 'Booker T., Washington, 87360, 373 781 7380, yellow' 
    expected = {
      "color": "yellow",
      "firstname": "Booker T.",
      "lastname": "Washington",
      "phonenumber": "373-781-7380",
      "zipcode": "87360"
    }

    format_parser = percolate.FormatParser3(inputted)
    self.assertEquals(format_parser.GetFormattedData(), expected)

  def testInvalidFormats(self):
    invalid_data = [
      'James Murphy, yellow, 83880, 018 154 6474',
      'Zlotnik, Zack, 123-456-7890, Blue, 12345',
      'Chandler, Kerri, (623)-668-9293, pink, 123123121',
      'asdfawefawea' 
    ]

    for item in invalid_data:
      parsed_data = percolate.FormatParser3(item).GetFormattedData()
      self.assertFalse(parsed_data)

if __name__ == '__main__':
  unittest.main()
