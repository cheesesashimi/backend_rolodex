#!/usr/bin/python

import json


class FormatParser(object):
    """Parent class for all formats to be parsed."""

    def __init__(self, entry):
        """Constructor.

        Args:
          data: string; The line from the given input file to parse.
        """
        self.entry = [item.strip() for item in entry.split(',')]

    def GetFormattedData(self):
        """Formats and returns the provided data, if valid.

        Returns:
          A dictionary of the data given if valid, False otherwise.
        """
        parsed_data = self.ParseFormat()
        if not parsed_data:
            return False

        phonenumber = self.FormatPhoneNumber(parsed_data['phonenumber'])
        if not phonenumber:
            return False
        parsed_data['phonenumber'] = phonenumber

        if not self.IsValidZipcode(parsed_data['zipcode']):
            return False

        return parsed_data

    def IsValidZipcode(self, zipcode):
        """Determines if a zipcode is valid.

        Args:
          zipcode: string; The zipcode to validate.

        Returns:
          True, if the zipcode is valid.
        """
        stripped_zipcode = strip_nonnumeric_characters(zipcode)
        return len(stripped_zipcode) == 5

    def FormatPhoneNumber(self, phonenumber):
        """Normalizes a phone number into a given format.

        Args:
          phonenumber: string; The phone number to format.

        Returns:
          The formatted phone number.
        """
        stripped_phone_number = strip_nonnumeric_characters(phonenumber)

        if len(stripped_phone_number) == 10:
            return '%s-%s-%s' % (stripped_phone_number[0:3],
                                 stripped_phone_number[3:6],
                                 stripped_phone_number[6:10])


class FormatParser1(FormatParser):
    """Parser for this format: Lastname, Firstname, (703)-742-0996, Blue, 10013
    """

    def ParseFormat(self):
        """Parses entry data.

        Returns:
          A dictionary of parsed data.
        """
        if len(self.entry) != 5:
            return False

        lastname, firstname, phonenumber, color, zipcode = self.entry
        return dict(lastname=lastname,
                    firstname=firstname,
                    phonenumber=phonenumber,
                    color=color,
                    zipcode=zipcode)


class FormatParser2(FormatParser):
    """Parser for this format: Firstname Lastname, Red, 11237, 703 955 0373
    """

    def ParseFormat(self):
        """Parses entry data.

        Returns:
          A dictionary of parsed data.
        """
        if len(self.entry) != 4:
            return False

        fullname, color, zipcode, phonenumber = self.entry
        splitname = fullname.split(' ')
        firstname = ' '.join(splitname[0:-1])
        lastname = splitname[-1]

        return dict(lastname=lastname,
                    firstname=firstname,
                    phonenumber=phonenumber,
                    color=color,
                    zipcode=zipcode)


class FormatParser3(FormatParser):
    """Parser for this format: Firstname, Lastname, 10013, 646 111 0101, Green
    """

    def ParseFormat(self):
        """Parses entry data.

        Returns:
          A dictionary of parsed data.
        """
        if len(self.entry) != 5:
            return False

        firstname, lastname, zipcode, phonenumber, color = self.entry

        return dict(lastname=lastname,
                    firstname=firstname,
                    phonenumber=phonenumber,
                    color=color,
                    zipcode=zipcode)


def strip_nonnumeric_characters(string_to_strip):
    return ''.join((character
                    for character in string_to_strip
                    if character.isdigit()))


def get_parsed_entry(entry_to_parse):
    """Runs an entry through each of the parsers to determine a match.

    Args:
      data_to_parse: string; The data to parse from the file.

    Returns:
      A dictionary of parsed data, if it matches one of the formats. False if not.
    """
    return (FormatParser1(entry_to_parse).GetFormattedData() or
            FormatParser2(entry_to_parse).GetFormattedData() or
            FormatParser3(entry_to_parse).GetFormattedData() or
            False)


def parse_data(data_to_parse):
    """Runs data through the various parsers to determine a match.

    Args:
      data_to_parse: list; A list of the data to parse.

    Returns:
      A dictionary containing the parsed entries and what lines of the file
      an error occurred on.
    """
    raw_entries = ((get_parsed_entry(entry), i)
                   for i, entry in enumerate(data_to_parse))

    entries = []
    errors = []

    for entry, line in raw_entries:
        if entry:
            entries.append(entry)
        else:
            errors.append(line)

    entries.sort(key=lambda entry: '%s %s' % (entry['lastname'],
                                              entry['firstname']))
    return dict(entries=entries, errors=errors)


def main():
    """The main body of the program."""
    with open('data.in', 'r') as input_file:
        with open('result.out', 'w') as output_file:
            parsed_data = parse_data(input_file)
            json_formatted_data = json.dumps(
                parsed_data, sort_keys=True, indent=2)
            output_file.write(json_formatted_data)


if __name__ == '__main__':
    main()
