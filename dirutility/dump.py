from argparse import ArgumentParser


class TextDump:
    def __init__(self, file_path, verbose=0):
        self.file_path = file_path
        self._verbose = verbose

    def printer(self, statement):
        if self._verbose > 0:
            print(statement)

    @staticmethod
    def _encode_data(data, split=None):
        """Encode data as a string in order to write to a text file."""
        data = data.split(split) if split else data
        if isinstance(data, (list, tuple, set)):
            return '\n'.join(data)
        else:
            return data

    def read(self):
        self.printer('Reading from text file `{}`'.format(self.file_path))
        with open(self.file_path, 'r') as txt:
            return txt.read()

    def write(self, data, split=None):
        self.printer('Writing to text file `{}`'.format(self.file_path))
        with open(self.file_path, 'w') as txt:
            return txt.write(self._encode_data(data, split))

    def append(self, data, split=None):
        self.printer('Appending to text file `{}`'.format(self.file_path))
        with open(self.file_path, 'a') as txt:
            return txt.write(self._encode_data(data, split))


def reader(file_path):
    """Read a text file and return its contents."""
    return TextDump(file_path).read()


def writer(file_path, data, split=None):
    """Write to a text file and return its contents."""
    return TextDump(file_path).write(data, split)


def appender(file_path, data, split=None):
    """Append a text file and return its contents."""
    return TextDump(file_path).append(data, split)


def main():
    """
    Example Usage:

    $ text-dump append --file-path domains.txt --data "dev.projects.hpadesign.com staging.projects.hpadesign.com beta.projects.hpadesign.com projects.localhost" --split ' '
    $ text-dump write --file-path domains.txt --data "dev.hpadesign.com staging.hpadesign.com beta.hpadesign.com public.localhost" --split ' '
    $ text-dump read --file-path domains.txt
    public.localhost"
    """
    # Declare argparse argument descriptions
    usage = 'Text dump utility.'
    description = 'Read, write and append text files.'
    helpers = {
        'file-path': "Path to text file to read/write to.",
        'data': "Data to write/append to the text file.",
        'split': "Character used separate a plain text list.",
    }

    # construct the argument parse and parse the arguments
    parser = ArgumentParser(usage=usage, description=description)
    sub_parser = parser.add_subparsers()

    # Read
    parser_read = sub_parser.add_parser('read')
    parser_read.add_argument('-f', '--file-path', help=helpers['file-path'], type=str)
    parser_read.set_defaults(func=reader)

    # Write
    parser_write = sub_parser.add_parser('write')
    parser_write.add_argument('-f', '--file-path', help=helpers['file-path'], type=str)
    parser_write.add_argument('-d', '--data', help=helpers['data'])
    parser_write.add_argument('-s', '--split', help=helpers['split'], type=str, default=None)
    parser_write.set_defaults(func=writer)

    # Append
    parser_write = sub_parser.add_parser('append')
    parser_write.add_argument('-f', '--file-path', help=helpers['file-path'], type=str)
    parser_write.add_argument('-d', '--data', help=helpers['data'])
    parser_write.add_argument('-s', '--split', help=helpers['split'], type=str, default=None)
    parser_write.set_defaults(func=appender)

    # Parse Arguments
    args = vars(parser.parse_args())
    func = args.pop('func')
    return func(**args)


if __name__ == '__main__':
    main()
