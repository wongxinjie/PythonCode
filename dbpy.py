##############################################################
#python中系统自带的数据持久化实现模块，可简单的实现部分数据库的功能。
# @coder: Xinjie Wong
# @Time: 2014/08/31
##############################################################
import dbhash
import shelve

def dbhash_sample():
	#打开一个文件，假如不存在则创建一个。
	db = dbhash.open('dbhash.dat', 'c')
	db['Tom'] = 'Beijing Road'
	db['Jerry'] = 'Shanghai Road'
	# db['Jim'] = 13 #出错，因为在dbhash模块中要求字典的键和值都必须是字符串。
	for k, v in db.iteritems():
		print k, v

	if db.has_key('Tom'):
		del db['Tom']
	print db
	db.close()

def shelve_sample():
	db = shelve.open('shelve.dat')
	db['Tom'] = ['Tom', 'male', 'USA', '171cm', '64kg', 21]
	db['Jimmy'] = ['Jimmy', 'male', 'China', '173cm', '72kg', 22]
	db['Jude'] = ['Jude', 'female', 'Taiwan', '165cm', '54kg', 20]
	#db[22] =['hell', '23', 22] #出错，因为在shelve模块中要求字段的键必须为字符串。
	print db
	db.close()

def main():
	dbhash_sample()
	shelve_sample()

if __name__ == '__main__':
	main()

	









