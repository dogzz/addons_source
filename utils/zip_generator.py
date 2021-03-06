# Script to generate the zip files required for <datadir zip="true"> in the
# addon.xml of a repository

import os
import xml.etree.ElementTree
import shutil
from zipfile import ZipFile

dir_with_script = 'utils'

class Generator:

	def __init__( self, *args, **kwargs ):
		# generate files
		self.version = kwargs.get('version')
		if self.version == '2.1.0':
			self.release_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'zip')
		elif self.version == '2.0':
			self.release_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'edem-addons')
		
		dirs = (os.listdir('.'))
		for addon_dir in dirs:
			if(not os.path.isdir(addon_dir)):
				continue		
			if(addon_dir.startswith('.')):
				# skip hidden dirs
				continue
			if(addon_dir in [dir_with_script]):
				# skip download directory
				continue
			self.create_zip_file(addon_dir)
			
	def get_plugin_version(self, addon_dir):
		addon_file = os.path.join(addon_dir, 'addon.xml')
		if not os.path.exists(self.release_dir + os.sep + addon_dir):
			os.mkdir(self.release_dir + os.sep + addon_dir)
		shutil.copyfile(addon_file, os.path.join(self.release_dir, addon_dir, 'addon.xml'))
		if os.path.exists(os.path.join(addon_dir, "icon.png")):
			shutil.copyfile(os.path.join(addon_dir, "icon.png"), os.path.join(self.release_dir, addon_dir, "icon.png"))
		if os.path.exists(os.path.join(addon_dir, "fanart.jpg")):
			shutil.copyfile(os.path.join(addon_dir, "fanart.jpg"), os.path.join(self.release_dir, addon_dir, "fanart.jpg"))
		try:
			data = open(addon_file, 'r').read()
			node = xml.etree.ElementTree.XML(data)
			if os.path.exists(os.path.join(addon_dir, "changelog.txt")):
				shutil.copyfile(os.path.join(addon_dir, "changelog.txt"), os.path.join(self.release_dir, addon_dir, "changelog-%s.txt" % node.get('version')))
			return(node.get('version'))
		except Exception as e:
			print 'Failed to open %s' % addon_file
			print e.message


	def create_zip_file(self, addon_dir):
		version = self.get_plugin_version(addon_dir)
		if not version:
			return
		with ZipFile(self.release_dir + os.sep + addon_dir + os.sep + addon_dir + '-' + version + '.zip',
								 'w') as addonzip:
			for root, dirs, files in os.walk(addon_dir):
				for file_path in files:
					if file_path.endswith('.zip') or file_path.endswith('.pyo') or file_path.endswith('.pyc') or file_path == 'Thumbs.db':
						continue
					if root.find('.git')>0 or root.find('.idea')>0:
						continue
					print "adding %s" % os.path.join(root, file_path) 
					addonzip.write(os.path.join(root, file_path))
			addonzip.close()

# if __name__ == '__main__':
#	main()
