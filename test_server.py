# run with:
# python -m unittest discover

import unittest
import json
import server

# Status Codes
HTTP_200_OK             = 200
HTTP_201_CREATED        = 201
HTTP_204_NO_CONTENT     = 204
HTTP_400_BAD_REQUEST    = 400
HTTP_404_NOT_FOUND      = 404
HTTP_409_CONFLICT       = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductServer(unittest.TestCase):
    def setUp(self):
        server.app.debug = True
        self.app = server.app.test_client()
        #server.products = { 1: {'id': 1, 'name': 'TV', 'category': 'entertainment', 'discontinued': True, 'price': 999}, 2: {'id': 2, 'name': 'Blender', 'category': 'appliances', 'discontinued': False, 'price': 99} }   

    def test_index(self):
        resp = self.app.get('/')
        self.assertTrue ('product Demo REST API Service' in resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
    
"""
    def test_get_product_list(self):
        resp = self.app.get('/products')
        self.assertTrue( resp.status_code == HTTP_200_OK )

        data = json.loads(resp.data)
        self.assertTrue( len(resp.data) > 0 ) 
        self.assertTrue(data[0]['name'] == 'TV')
        self.assertTrue(data[1]['name'] == 'Blender')

    def test_get_product_price(self):
        resp_min_price = self.app.get('/products?min-price=100')
        self.assertTrue( resp_min_price.status_code == HTTP_200_OK )
        data_min_price = json.loads(resp_min_price.data)
        self.assertTrue(data_min_price[0]['name'] == 'TV')
        
        resp_max_price = self.app.get('/products?max-price=100')
        self.assertTrue( resp_max_price.status_code == HTTP_200_OK )
        data_max_price = json.loads(resp_max_price.data)
        self.assertTrue(data_max_price[0]['name'] == 'Blender')

    def test_get_product_limit(self):
        resp = self.app.get('/products?limit=1')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue( len(data) == 1)

    def test_get_product_category(self):
        resp = self.app.get('/products?category=entertainment')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue(data[0]['name'] == 'TV')

    def test_get_product(self):
        resp = self.app.get('/products/2')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        data = json.loads(resp.data)
        self.assertTrue (data['name'] == 'Blender')

    def test_query_product_list(self):
        self.setup_test_by_attribute('category', 'entertainment')
        self.setup_test_by_attribute('discontinued', True)  
        self.setup_test_by_attribute('price', 999)  

    def test_create_product(self):
        # save the current number of products for later comparison
        product_count = self.get_product_count()
        # add a new product
        new_product = {'name': 'toaster', 'category': 'kitchen appliances', 'price': 99}
        data = json.dumps(new_product)
        resp = self.app.post('/products', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_201_CREATED )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['name'] == 'toaster')
        # check default value of 'discontinued' is 'False'
        self.assertTrue (new_json['discontinued'] == False)
        # check the price of the product
        self.assertTrue (new_json['price'] == 99)
        # check that count has gone up and includes sammy
        resp = self.app.get('/products?limit=' + str(product_count + 1))
        data = json.loads(resp.data)
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(data) == product_count + 1 )
        self.assertTrue( new_json in data )

    def test_update_product(self):
        new_Blender = {'name': 'Blender', 'category': 'home appliances', 'discontinued': True, 'price': 99}
        data = json.dumps(new_Blender)
        resp = self.app.put('/products/2', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['category']       == 'home appliances')
        self.assertTrue (new_json['discontinued']   == True)
        self.assertTrue (new_json['price']          == 99)
    
    def test_discontinue_produce(self):
        resp = self.app.put('/products/2/discontinue')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        new_json = json.loads(resp.data)
        self.assertTrue (new_json['discontinued']   == True)

    def test_update_product_with_no_name(self):
        new_product = {'category': 'entertainment'}
        data = json.dumps(new_product)
        resp = self.app.put('/products/2', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_delete_product(self):
        # save the current number of products for later comparrison
        product_count = self.get_product_count()
        # delete a product
        resp = self.app.delete('/products/2', content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_204_NO_CONTENT )
        self.assertTrue( len(resp.data) == 0 )
        new_count = self.get_product_count()
        self.assertTrue ( new_count == product_count - 1)

    def test_create_product_with_no_name(self):
        new_product = {'category': 'entertainment'}
        data = json.dumps(new_product)
        resp = self.app.post('/products', data=data, content_type='application/json')
        self.assertTrue( resp.status_code == HTTP_400_BAD_REQUEST )

    def test_get_nonexisting_product(self):
        resp = self.app.get('/products/5')
        self.assertTrue( resp.status_code == HTTP_404_NOT_FOUND )

######################################################################
# Utility functions
######################################################################

    def get_product_count(self):
        # save the current number of products
        resp = self.app.get('/products')
        self.assertTrue( resp.status_code == HTTP_200_OK )
        # print 'resp_data: ' + resp.data
        data = json.loads(resp.data)
        return len(data)

    def setup_test_by_attribute(self, attr_name, attr_value):
        resp = self.app.get('/products', \
                            query_string='attr_name=attr_value'.format(attr_name=attr_name, attr_value=attr_value))
        self.assertTrue( resp.status_code == HTTP_200_OK )
        self.assertTrue( len(resp.data) > 0 )
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertTrue(query_item[attr_name] == attr_value) 
######################################################################
#   M A I N
######################################################################
"""
if __name__ == '__main__':
    unittest.main()