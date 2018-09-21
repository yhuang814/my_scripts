from xml_mgr import Xml_Mgr

import sys
import json
import shutil, errno, os
import os.path
import untangle


def get_file_path() : 
    script_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = script_dir + '/test_data/test_01.xml'
    return file_path

def main():
    file_path = get_file_path()

    obj = untangle.parse(file_path)

    contents = obj.library.content

    fs_assets = []

    for content in contents:

        #content asset ID
        content_id = content['content-id']

        is_fs_asset = False #indicates if content asset if managed by FS

        #Custom attributes of each content assets
        custom_attributes = content.custom_attributes.custom_attribute
        
        for attribute in custom_attributes : 
            attribute_id = attribute['attribute-id']
            
            if attribute_id == 'fsGenerationTime' and attribute.cdata:
                is_fs_asset = True
                fs_assets.append(content_id)
            #if attribute_id == 'fsConfig':
            #print(attribute.cdata) #attribute data

    print(fs_assets)

if __name__ == '__main__':
    	main()
        