'''
key_file: for key storing
including one message digestor, and file writer

'''

class key_file:
    file_name=''
    def __init__(file_name):
        f=open(file_name,"w+")
        self.file_name=file_name
        f.close()
    def update(key_key, key_value):
        '''
        update with the value passed in, user should know what he is doing
        public:p,q,a,b
        private:d
        '''
        f.open(self.file_name)
        f.write(key_key)
        f.write(':')
        f.write(self.key_value)
        f.close()
    def digest():
        '''
        return the value of key file with dictionary
        '''        