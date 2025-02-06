import json
from django.core.management.base import BaseCommand
from quiz.models import Course

class Command(BaseCommand):
    help = 'Import course data from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The JSON file to import')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        
        try:
            with open(json_file, 'r') as file:
                courses_data = json.load(file)
                for course_data in courses_data:
                    # Remove the 'course' field if it exists
                    course_data.pop('course', None)
                    Course.objects.create(**course_data)
                
            self.stdout.write(self.style.SUCCESS('Course data imported successfully.'))
        
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File "{json_file}" not found.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON. Please check the file format.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
