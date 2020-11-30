import os

class SchemaFile:
  
  @classmethod
  def write(cls, filename, content, directory, ext='.sql'):
    directory = os.path.abspath(directory)
    if not os.path.isdir(directory):
      os.mkdir(directory)
    filename = '{}/{}{}'.format(directory, filename, ext)
    with open(filename, 'w') as f:
      f.write(content)

  @classmethod
  def read(cls, filename, directory, ext='.sql'):
    filename = '{}/{}{}'.format(directory, filename, ext)
    filename = os.path.abspath(filename)
    with open(filename) as f:
      return f.read()

