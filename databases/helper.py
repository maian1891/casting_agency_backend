from databases.models import Actor, Movie 
from databases.data import dummy_actor_data, dummy_movie_data
  
class UserHelper: 
    def add_dummy_actor_data(): 
        ''' 
        Function to add dummy actor data into Table 
        arg : dummy_actor_data which is list of  
        actor info which we want to add 
        '''
        for data in dummy_actor_data: 
            user_obj = Actor(*data) 
            user_obj.insert() 
        print("Successfully Added") 
  
    def add_dummy_movie_data(): 
        ''' 
        Function to add dummy user data into Table 
        arg : seed_data which is list of  
        user info which we want to add 
        '''
        for data in dummy_movie_data: 
            user_obj = Movie(*data) 
            user_obj.insert() 
        print("Successfully Added") 
  