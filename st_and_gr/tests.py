from django.test import TestCase
  
class Login_Test(TestCase):
    def test_login(self):
        response = self.client.post('/', {'username': 'nikita', 'password': 'nikita'})
        self.assertEqual(response.status_code, 200) 

class Create_Group_Test(TestCase):                                                            
    def test_create_group_form(self):                                                                      
        response = self.client.post('/group/create/',{'group_name': 'group 3'}) 
        self.assertEqual(response.status_code, 302) 
        
class Add_Student_Test(TestCase):                                                                                
    def test_add_student_form(self):                                               
        response = self.client.post('/student/add/',{'full_name': 'Novikov Sergey Viktorovich',
                                    'date_of_birth': '12.10.1990','student_id_number': '12744','group': 'group 3'})
        self.assertEqual(response.status_code, 302)  
                                         