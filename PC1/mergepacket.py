from filesplit.merge import Merge

mergercv = Merge(str(os.getcwd())+'\Receive', str(os.getcwd())+'\Receive', 'output'+filepath.suffix)
mergexmt = Merge(filepath, filepath, filepath.name)