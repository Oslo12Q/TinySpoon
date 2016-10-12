#coding=utf-8
from django.test import TestCase
from django.core.files import File
from childrenrecipe.manager import get_recipe, create_category, create_tag, create_recipe
from django.test import Client
from .models import *
import json
import datetime
import exceptions
# Create your tests here.



class RecommendTests(TestCase): 
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_recommend_view_without_data(self):
        recommend_response = self.client.get('/api/recommend/')
        recommend_response_content = recommend_response.content
        self.assertEqual(recommend_response.status_code, 200)

    def test_recommend_view_with_only_future_pubdate(self):
        pass


    def test_recommend_view(self):
        #import pdb
        #pdb.set_trace()
        now = datetime.datetime.now()
        epoch = datetime.datetime(1970, 1, 1)+datetime.timedelta(hours=8)
        td = now - epoch
        timestamp_recipe_createtime = int(td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)
        
        with open("./images/exhibited_picture/image1.png", 'rb') as imagefile1:
            django_file1 = File(imagefile1)

            age_category = Category.objects.create(
                name = 'Age',
                is_tag = 1,
                seq = 1
            )
            
            trophic_category = Category.objects.create(
                name = 'Nutrition Classification',
                is_tag = 0,
                seq = 2
            )

            therapeutic_category = Category.objects.create(
                name = 'Therapeutic Classification',
                is_tag = 0,
                seq = 3
            )

            cookmethod_category = Category.objects.create(
                name = 'Cooking Method',
                is_tag = 0,
                seq = 4
            )

            tag1 = Tag.objects.create(
                name = 'breakfast',
                category = Category.objects.create(
                    name = 'Scene Classification',
                    is_tag = 0,
                    seq = 2
                ),
                seq = 1
            )

            tag2 = Tag.objects.create(
                name = 'Zinc supplement',
                category = trophic_category,
                seq = 2
            )

            tag3 = Tag.objects.create(
                name = 'cough',
                category = therapeutic_category,
                seq = 4
            )

            tag4 = Tag.objects.create(
                name = 'boil',
                category = cookmethod_category,
                seq = 3
            )

            recipe1 = Recipe.objects.create(
                    name = 'lotus mung bean porridge',
                    user = 'cyanlime',
                    introduce = 'delicious',
                    tips = 'a bit of sugar',
            )
            recipe1.tag.add(tag1)
            recipe1.save()
            recipe1.exihibitpic.save("recommend_image2.png", django_file1, save=True)

            recommend1 = Recommend.objects.create(
                recipe = recipe1,
                pubdate = datetime.datetime.now()-datetime.timedelta(hours=1)
            )
            recommend1.image.save("recommend_image1.png", django_file1, save=True)

            material = Material.objects.create(
                recipe = recipe1,
                name = 'artichoke',
                portion = '10g'
            )

            procedure1 = Procedure.objects.create(
                recipe = recipe1,
                seq = 1,
                describe = 'washup'
            )
            procedure1.image.save("recommend_image3.png", django_file1, save=True)

            procedure2 = Procedure.objects.create(
                recipe = recipe1,
                seq = 2,
                describe = 'braise'
            )
            procedure2.image.save("recommend_image4.png", django_file1, save=True)

            procedure3 = Procedure.objects.create(
                recipe = recipe1,
                seq = 3, 
                describe = 'stew' 
            )
            procedure3.image.save("recommend_image5.png", django_file1, save=True)

        import pdb
        pdb.set_trace()
        recommend_response = self.client.get('/api/recommend/')
        recommend_response_content = recommend_response.content
        self.assertEqual(recommend_response.status_code, 200)
        self.assertGreater(recommend_response_content.get('pubdate'), recommend_response_content.get('create_time'))
        self.assertLess(recommend_response_content.get('recipe').get('create_time'), recommend_response_content.get('pubdate'))
        self.assertLess(recommend_response_content.get('recipe').get('create_time'), recommend_response_content.get('create_time'))

        recommend_image_url = recommend_response_content.get('image')
        recommend_image_response = self.client.get(recommend_image_url)
        self.assertEqual(recommend_image_response.status_code, 200)

        recommend_fields = ['recipe', 'image', 'create_time', 'pubdate']
        recommend_recipe_fields = ['name', 'url', 'introduce', 'create_time', 'user', 'id']
        for field in recommend_fields:
            self.assertIn(field, recommend_response_content)
        for field2 in recommend_recipe_fields:
            self.assertIn(field2, recommend_response_content.get('recipe'))
                
        recommend_recipe_exihibitpic_url = recommend_response_content.get('recipe').get('exihibitpic')
        recommend_recipe_exihibitpic_response = self.client.get('recommend_recipe_exihibitpic_url')
        self.assertEqual(recommend_recipe_exihibitpic_response.status_code, 200)

        recommend_recipe_url = recommend_response_content.get('recipe').get('url')
        recommend_recipe_response = self.client.get(recommend_recipe_url)
        self.assertEqual(recommend_recipe_response.status_code, 200)

        recipe_fields = ['url', 'id', 'name', 'user', 'exihibitpic', 'introduce', 'tags', 'tips',
                'material', 'procedure', 'width', 'height']
        recipe_tags_fields = ['name', 'category_name']
        recipe_material_fields = ['url', 'id', 'recipe_title', 'name', 'portion']
        recipe_procedure_fields = ['url', 'id', 'recipe', 'seq', 'describe', 'image', 'width', 'height']
                
        
        recommend_recipe_response_content = json.loads(recommend_recipe_response.content)
        for field3 in recipe_fields:
            self.assertIn(field3, recommend_recipe_response_content)
        self.assertEqual(recommend_response_content.get('recipe').get('id'), recommend_recipe_response_content.get('id'))
        self.assertEqual(recommend_response_content.get('recipe').get('url'), recommend_recipe_response_content.get('url'))
        self.assertEqual(recommend_response_content.get('recipe').get('create_time'), recommend_recipe_response_content.get('create_time'))
        self.assertEqual(recommend_response_content.get('recipe').get('name'), recommend_recipe_response_content.get('name'))
        self.assertEqual(recommend_response_content.get('recipe').get('user'), recommend_recipe_response_content.get('user'))

        for field4 in recipe_tags_fields:
            self.assertIn(field4, recommend_recipe_response_content.get('tags'))

        material_content = recommend_recipe_response_content.get('material')
        procedure_content = recommend_recipe_response_content.get('procedure')
        
        for item in range(0, len(material_content)):
            for field5 in recipe_material_fields:
                self.assertIn(field5, material_content[item])
            self.assertEqual(material_content[item].get('recipe_title'), recommend_recipe_response_content.get('name'))                   
            if len(material_content)>1:
                self.assertLess(material_content[item-1].get('id')+1, material_content[item].get('id'))
            
            material_url = material_content[item].get('url')
            material_response = self.client.get(material_url)
            self.assertEqual(material_response.status_code, 200)
            
            material_response_content = material_response.content
            for field6 in recipe_material_fields:
                self.assertIn(field6, material_response_content)
            self.assertEqual(material_response_content.get('id'), material_content[item].get('id'))
            materialins_url = material_response_content.get('url')
            materialins_response = self.client.get(materialins_url)
            self.assertEqual(materialins_response.status_code, 200)
        
                    
        for item2 in range(0, len(procedure_content)):
            for field7 in recipe_procedure_fields:
                self.assertIn(field7, procedure_content[item2])
            self.assertEqual(procedure_content[item2].get('recipe'), recommend_recipe_response_content.get('name'))   
            if len(procedure_content)>1:    
                self.assertEqual(procedure_content[item-1].get('seq')+1, procedure_content[item].get('seq'))

            procedure_url = procedure_content[item2].get('url')
            procedure_response = self.client.get(procedure_url)
            self.assertEqual(procedure_response.status_code, 200)

            procedure_image_url = procedure_content[item2].get('image')
            if procedure_image_url:
                procedure_image_response = self.client.get(procedure_image_url)
                self.assertEqual(procedure_image_response.status_code, 200)
            else:
                pass
        
            procedure_response_content = procedure_response.content
            for field8 in recipe_procedure_fields:
                self.assertIn(field8, procedure_response_content)
            self.assertEqual(procedure_response_content.get('id'), procedure_content[item2].get('id'))
            self.assertEqual(procedure_response_content.get('seq'), procedure_content[item2].get('seq'))
            procedureins_url = procedure_response_content.get('url')
            procedureins_response = self.client.get(procedureins_url)
            self.assertEqual(procedureins_response.status_code, 200)


    def test_recommend_without_recipe(self):
        pass

    def test_recommend_view_without_image(self):
        pass

    def test_recommend_view_without_pubdate(self):
        pass


class TagsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_tags_view_without_data(self):
        tags_response = self.client.get('/api/tags')
        tags_response_content = tags_response.content
        self.assertEqual(tags_response.status_code, 200)
        #self.assertIsInstance(tags_response_content, list)
        #self.assertEqual(list(tags_response_content), [])

    def test_tags_view(self):       
        age_category = Category.objects.create(
            name = 'Age',
            is_tag = 1,
            seq = 1
        )
            
        trophic_category = Category.objects.create(
            name = 'Nutrition Classification',
            is_tag = 0,
            seq = 2
        )

        therapeutic_category = Category.objects.create(
            name = 'Therapeutic Classification',
            is_tag = 0,
            seq = 3
        )

        cookmethod_category = Category.objects.create(
            name = 'Cooking Method',
            is_tag = 0,
            seq = 4
        )

        tag5 = Tag.objects.create(
            name  = '4 month',
            category = age_category,
            seq = 1
        )

        tag1 = Tag.objects.create(
            name = 'breakfast',
            category = Category.objects.create(
                name = 'Scene Classification',
                is_tag = 0,
                seq = 5
            ),
            seq = 2
        )

        tag2 = Tag.objects.create(
            name = 'Zinc supplement',
            category = trophic_category,
            seq = 2
        )

        tag3 = Tag.objects.create(
            name = 'cough',
            category = therapeutic_category,
            seq = 4
        )

        tag4 = Tag.objects.create(
            name = 'boil',
            category = cookmethod_category,
            seq = 3
        )
        
        #import pdb
        #pdb.set_trace()
        tags_response = self.client.get('/api/tags')
        self.assertEqual(tags_response.status_code, 200)
        tags_response_content = tags_response.content
        tags_response_data = tags_response.data
        self.assertIsInstance(tags_response_content, str)
        self.assertIsInstance(tags_response_data, list)
        

        categorys_fields = ['category', 'seq', 'tags']
        tags_fields = ['tag', 'id']
        for item in range(0, len(tags_response_data)):
            for field in categorys_fields:
                self.assertIn(field, tags_response_data[item])
                self.assertIsInstance(tags_response_data[item].get('tags'), list)
                #if len(tags_response_content)>1:
                    #self.assertEqual(tags_response_content[item-1].get('seq')+1, 
                        #tags_response_content[item].get('seq'))
            tags_content = tags_response_data[item].get('tags')
            for item2 in range(0, len(tags_content)):
                for field2 in tags_fields:
                    self.assertIn(field2, tags_content[item2]) 
        
    def test_tags_view_with_category_age_data_only(self):
        age_category = Category.objects.create(
            name = 'Age',
            is_tag = 1,
            seq = 1
        )
        tag = Tag.objects.create(
            name  = '4 month',
            category = age_category,
            seq = 1
        )
        tags_response = self.client.get('/api/tags')
        self.assertEqual(tags_response.status_code, 200)
        self.assertIsInstance(tags_response.data, list)
        self.assertEqual(list(tags_response.data), [])
    
    def test_tags_view_without_category_age_data(self):
        pass

    def test_tags_view_without_category_data(self):
        pass

    def test_tags_view_with_category_data_only(self):
        pass


class RecipesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass     

    def test_recipe_view_without_data_without_param(self):
        import pdb
        pdb.set_trace()
        recipe_response = self.client.post('/api/recipe')
        recipe_response_data = recipe_response.data
        self.assertEqual(recipe_response.status_code, 200)
        self.assertIsInstance(recipe_response_data, list)
        self.assertEqual(recipe_response_data, [])


    def test_recipe_view_without_param(self):
        import pdb
        pdb.set_trace()
        with open("./images/exhibited_picture/image1.png", 'rb') as imagefile2:
            django_file2 = File(imagefile2)

            age_category = Category.objects.create(
                name = 'Age',
                is_tag = 1,
                seq = 1
            )
            
            trophic_category = Category.objects.create(
                name = 'Nutrition Classification',
                is_tag = 0,
                seq = 2
            )

            therapeutic_category = Category.objects.create(
                name = 'Therapeutic Classification',
                is_tag = 0,
                seq = 3
            )

            cookmethod_category = Category.objects.create(
                name = 'Cooking Method',
                is_tag = 0,
                seq = 4
            )

            tag1 = Tag.objects.create(
                name = 'breakfast',
                category = Category.objects.create(
                    name = 'Scene Classification',
                    is_tag = 0,
                    seq = 1
                ),
                seq = 1
            )

            tag2 = Tag.objects.create(
                name = 'Zinc supplement',
                category = trophic_category,
                seq = 2
            )

            tag3 = Tag.objects.create(
                name = 'cough',
                category = therapeutic_category,
                seq = 4
            )

            tag4 = Tag.objects.create(
                name = 'boil',
                category = cookmethod_category,
                seq = 3
            )

            recipe1 = Recipe.objects.create(
                    name = 'lotus mung bean porridge',
                    user = 'cyanlime',
                    introduce = 'delicious',
                    tips = 'a bit of sugar',
            )
            recipe1.tag.add(tag1)
            recipe1.save()
            recipe1.exihibitpic.save("recipe1_exihibitpic.png", django_file2, save=True)

            material = Material.objects.create(
                recipe = recipe1,
                name = 'artichoke',
                portion = '10g'
            )

            procedure1 = Procedure.objects.create(
                recipe = recipe1,
                seq = 1,
                describe = 'washup'
            )
            procedure1.image.save("procedure1_image.png", django_file2, save=True)

            procedure2 = Procedure.objects.create(
                recipe = recipe1,
                seq = 2,
                describe = 'braise'
            )
            procedure2.image.save("procedure2_image.png", django_file2, save=True)

            procedure3 = Procedure.objects.create(
                recipe = recipe1,
                seq = 3, 
                describe = 'stew' 
            )
            procedure3.image.save("procedure3_image.png", django_file2, save=True)
    
        import pdb
        pdb.set_trace()

        recipe_response = self.client.post('/api/recipe')
        recipe_response_data = recipe_response.data
        recipe_response_content = recipe_response.content
        self.assertEqual(recipe_response.status_code, 200)
        self.assertIsInstance(recipe_response_data, list)
        self.assertIsInstance(recipe_response_content, str)
        self.assertLessEqual(len(recipe_response_data), 10)
        sort_recipes_fields = ['age', 'recipes']
        recipes_fields = ['url', 'id', 'recipe', 'create_time', 'user', 'exihibitpic', 'introduce', 
                'tag', 'tips']
        tag_fields = ['name', 'category_name']

        for item in range(0, len(recipe_response_data)):
            for field in recipes_fields:
                self.assertIn(field, recipe_response_data[item])
            recipes_content = recipe_response_data[item].get('recipes')
            self.assertIsInstance(recipes_content, list)
            self.assertLessEqual(len(recipes_content), 10)
            for item2 in recipes_content:
                for field2 in recipes_fields:
                    self.assertIn(field2, recipes_content[item2])
                if len(recipes_content)>1:
                    self.assertGreater(recipes_content[item2-1].get('create_time'),
                            recipes_content[item2].get('create_time'))
                exihibitpic_url = recipes_content[item2].get('exihibitpic')
                exihibitpic_response = self.client.get(exihibitpic_url)
                self.assertEqual(exihibitpic_response.status_code, 200)

                #exhibitpic content_type
                
                tags_content = recipes_content[item2].get('tag')
                self.assertIsInstance(tags_content, list)
                for item3 in range(0, len(tags_content)):
                    for field3 in tags_fields:
                        self.assertIn(field3, tags_content[item3])
                    
                recipe_url = recipes_content[item2].get('url')
                recipe_response = self.client.get(recipe_url)
                self.assertEqual(recipe_response.status_code, 200)
                #Todo test recipe instance

                recipe_fields = ['url', 'id', 'name', 'user', 'exihibitpic', 'introduce', 
                        'tags', 'tips', 'material', 'procedure', 'width', 'height']
                tags_fields = ['name', 'category_name']
                material_fields = ['url', 'id', 'recipe_title', 'name', 'portion']
                procedure_fields = ['url', 'id', 'recipe', 'name', 'seq', 'describe', 'image',
                        'width', 'height']

                for item4 in range(0, len(recipe_response_content)):
                    for field4 in recipes_fields:
                        self.assertIn(field4, recipe_response_content[item4])
        
                    recipe_exihibitpic_url = recipe_response_content[item4].get('exihibitpic')
                    recipe_exihibitpic_response = self.client.get(recipe_exihibitpic_url)
                    self.assertEqual(recipe_exihibitpic_response.status_code, 200)

                    #content_type = 'image/jpeg'

                    tags_content = recipes_response_content[item4].get('tags')
                    for field5 in tags_fields:
                        self.assertIn(field5, tags_content)

                    material_content = recipes_response_content[item4].get('material')
                    for item5 in range(0, len(material_content)):
                        for field6 in material_fields:
                            self.assertIn(field6, material_content[item5])
                            if len(material_content)>1:
                                self.assertGreater(material_content[item5].get('id'), 
                                        material_content[item5-1].get('id'))
                                self.assertEqual(material_content[item5].get('recipe_title'),
                                        material_content[item5-1].get('recipe_title'))
                            material_url = material_content[item5].get('url')
                            material_response = self.client.get(material_url)
                            material_response_content = material_response.content
                            self.assertEqual(material_response.status_code, 200)
                            for field7 in material_response_content:
                                self.assertIn(field7, material_response_content)
                            self.assertEqual(material_response_content.get('id'), 
                                material_content[item5].get('id'))
                            materialins_url = material_response_content.get('url')
                            materialins_response = self.client.get(materialins_url)
                            self.assertEqual(materialins_response.status_code, 200)

                    procedure_content = recipes_response_content[item4].get('procedure')
                    self.assertIsInstance(procedure_content, list)
                    for item6 in range(0, len(procedure_content)):
                        for field8 in procedure_fields:
                            self.assertIn(field8, procedure_content[item6])
                            if len(procedure_content)>1:
                                self.assertGreater(procedure_content[item6].get('id'),
                                        procedure_content[item6-1].get('id'))
                                self.assertEqual(procedure_content[item6].get('recipe_name'),
                                        procedure_content[item6-1].get('recipe_name'))
                                self.assertEqual(procedure_content[item6-1].get('seq')+1,
                                        procedure_content[item6].get('seq'))
                        procedure_url = procedure_content[item6].get('url')
                        procedure_response = self.client.get(procedure_url)
                        self.assertEqual(procedure_response.status_code, 200)
                        procedure_response_content = procedure_response.content
                        for field8 in procedure_fields:
                            self.assertIn(field8, procedure_response_content)
                        self.assertEqual(procedure_response_content.get('id'), 
                                procedure_content[item6].get('id'))
                        self.assertEqual(procedure_response_content.get('seq'),
                                procedure_content[item6].get('seq'))
                        procedureins_url = procedure_response_content.get('url')
                        procedureins_response = self.client.get(procedureins_url)
                        self.assertEqual(procedureins_response.status_code, 200)

    def test_recipe_view_with_age_param(self):
        with open("./images/exhibited_picture/image1.png", 'rb') as imagefile3:
            django_file3 = File(imagefile3)

            age_category = Category.objects.create(
                name = 'Age',
                is_tag = 1,
                seq = 1
            )
            
            trophic_category = Category.objects.create(
                name = 'Nutrition Classification',
                is_tag = 0,
                seq = 2
            )

            tag1 = Tag.objects.create(
                name = '5 month',
                category = age_category,
                seq = 2
            )

            recipe1 = Recipe.objects.create(
                    name = 'lotus mung bean porridge',
                    user = 'cyanlime',
                    introduce = 'delicious',
                    tips = 'a bit of sugar',
            )
            recipe1.tag.add(tag1)
            recipe1.save()
            recipe1.exihibitpic.save("recipe1_exihibitpic.png", django_file3, save=True)

        import pdb
        pdb.set_trace()

        tag_id = str(tag1.id)
        payload = {"tag_id": tag_id}
        #payload = {'age': tag1.id, 'content_type': 'application/json'}
        recipes_response = self.client.post('/api/recipe', data=payload, content_type='application/json' )
        self.assertEqual(recipes_response.status_code, 200)


    def test_recipe_view_with_tagid_param(self):
        with open("./images/exhibited_picture/image1.png", 'rb') as imagefile4:
            django_file4 = File(imagefile4)

            age_category = Category.objects.create(
                name = 'Age',
                is_tag = 1,
                seq = 1
            )
            
            trophic_category = Category.objects.create(
                name = 'Nutrition Classification',
                is_tag = 0,
                seq = 2
            )

            tag1 = Tag.objects.create(
                name = 'Zinc supplement',
                category = trophic_category,
                seq = 2
            )

            recipe1 = Recipe.objects.create(
                    name = 'lotus mung bean porridge',
                    user = 'cyanlime',
                    introduce = 'delicious',
                    tips = 'a bit of sugar',
            )
            recipe1.tag.add(tag1)
            recipe1.save()
            recipe1.exihibitpic.save("recipe1_exihibitpic.png", django_file4, save=True)

        import pdb
        pdb.set_trace()

        tag_id = int(tag1.id)
        payload = {"age": [tag_id]}
        recipes_response = self.client.post('/api/recipe', data=payload, content_type='application/json')
        self.assertEqual(recipes_response.status_code, 200)    


    def test_recipe_view_without_category_age_data(self):
        with open("./images/exhibited_picture/image1.png", 'rb') as imagefile3:
            django_file3 = File(imagefile3)
            
            trophic_category = Category.objects.create(
                name = 'Nutrition Classification',
                is_tag = 0,
                seq = 2
            )

            tag1 = Tag.objects.create(
                name = 'Zinc supplement',
                category = trophic_category,
                seq = 1
            )

            recipe1 = Recipe.objects.create(
                    name = 'lotus mung bean porridge',
                    user = 'cyanlime',
                    introduce = 'delicious',
                    tips = 'a bit of sugar',
            )
            recipe1.tag.add(tag1)
            recipe1.save()
            recipe1.exihibitpic.save("recipe1_exihibitpic.png", django_file3, save=True)


            recipe_response = self.client.post('/api/recipe', data={}, content_type='application/json')




    def test_recipe_view_with_more_than_one_category_age_data(self):
        pass


    def test_recipe_view_pagination(self):
        pass

    def test_search_recipe_view_with_one_tag(self):
        pass


    def test_search_recipe_view_with_more_than_one_tag(self):
        pass

    def test_search_recipe_view_with_no_category_age_data(self):
        pass

    def test_search_recipe_view_with_one_category_age_data(self):
        pass

    def test_search_recipe_view_with_more_than_one_category_age_data(self):
        pass

    
