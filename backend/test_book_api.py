import unittest
import requests
import uuid

class BookAPI(unittest.TestCase):
    URL = "http://127.0.0.1:5000"
    
    #id = uuid.uuid4().hex
    
    data ={
            "author": "Chinua Achebe",
            "rating": 5,
            "title": "Things fall apart"
        }
      
    updated_data = {"rating": 2}
   
   
    def test_1_post_book(self):
        response = requests.post(self.URL + "/books", json=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        print("Test 1 successfully completed")

    def test_2_post_book_with_no_entry_data(self):
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.URL + "/books",  headers=headers)
        self.assertEqual(response.status_code, 400)
        print("Test 2 successfully completed")

    def test_3_get_all_books(self):
        response =  requests.get(self.URL + "/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)
        print("Test 3 successfully completed")

    def test_4_get_all_books_from_unknown_endpoint(self):
        response =  requests.get(self.URL + "/book")
        self.assertEqual(response.status_code, 404)
        print("Test 4 successfully completed")

    def test_5_get_specific_book(self):
        response = requests.get(self.URL + "/books/2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["title"] == "Asymmetry: A Novel")
        print("Test 5 successfully completed")
    
    def test_6_get_specific_book_returns_no_book_found(self):
        response = requests.get(self.URL + "/books/10000")
        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.json()["error_message"] == "Resource not found")
        print("Test 6 successfully completed")

    def test_7_update_book(self):
        response = requests.patch(self.URL + "/books/1", json=self.updated_data)
        self.assertEqual(response.json().get("updated_rating"), self.updated_data["rating"])
        self.assertEqual(response.status_code, 200)
        print("Test 7 successfully completed")

    def test_8_update_book_returns_no_book_found(self):
        response = requests.patch(self.URL + "/books/404", json=self.updated_data)
        self.assertEqual(response.json().get("error_message"), "Resource not found")
        self.assertEqual(response.status_code, 404)
        print("Test 8 successfully completed")

    def test_9_delete_book(self):
       #Get book by id
       response = requests.get(self.URL + "/books")
       book_id = response.json()["books"][-1]["id"]
       
       #Delete book by id
       response = requests.delete(self.URL + f"/books/{book_id}")
       self.assertEqual(response.status_code, 200)
       self.assertTrue(response.json()["deleted_book_id"] == book_id)
       print("Test 9 successfully completed")
        

if __name__ == "__main__": 
    tester = BookAPI()

    tester.test_1_post_book()
    tester.test_2_post_book_with_no_entry_data()
    tester.test_3_get_all_books()
    tester.test_4_get_all_books_from_unknown_endpoint()
    tester.test_5_get_specific_book()
    tester.test_6_get_specific_book_returns_no_book_found()
    tester.test_7_update_book()
    tester.test_8_update_book_returns_no_book_found()
    tester.test_9_delete_book()
    
    
    
  
    
   