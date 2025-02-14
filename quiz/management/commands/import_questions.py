import json
from django.core.management.base import BaseCommand
from quiz.models import Question, Course

class Command(BaseCommand):
    help = 'Import question data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to import')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        
        print(f"Attempting to import questions from: {json_file}")  # Debugging output
        
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
                print(f"Loaded JSON data: {data}")  # Debugging output for loaded data
                questions_data = data  # Directly use the loaded list of questions

                for question_data in questions_data:
                    # Get the course instance
                    course_id = question_data.get('course_id')  # Use get to avoid KeyError


                    if course_id:
                        try:
                            course = Course.objects.get(id=course_id)
                        except Course.DoesNotExist:
                            self.stdout.write(self.style.ERROR(f'Course with id {course_id} does not exist. Skipping question.'))
                            continue
                    else:
                        self.stdout.write(self.style.ERROR('Course ID not provided. Skipping question.'))
                        continue
                    
                    # Create the Question instance
                    Question.objects.create(course=course, **question_data)
                
            self.stdout.write(self.style.SUCCESS('Question data imported successfully.'))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{json_file}" not found.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON. Please check the file format.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
