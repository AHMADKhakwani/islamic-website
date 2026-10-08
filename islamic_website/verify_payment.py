import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'islamic_website.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from islamic_app.views import payment_success, course_detail
from islamic_app.models import Course, Enrollment

# Create test data
user, _ = User.objects.get_or_create(username='testuser', email='test@example.com')
course = Course.objects.get(id=1)

# Simulate request to payment_success
factory = RequestFactory()
request = factory.get(f'/payment-success/{course.id}/')
request.user = user

print(f"Testing payment_success for user: {user.username}, course: {course.title}")

# Call the view
response = payment_success(request, course.id)

# Check redirection
if response.status_code == 302 and response.url == f'/course/{course.id}/':
    print("SUCCESS: Redirected to course detail page.")
else:
    print(f"FAILURE: Unexpected response status {response.status_code} or url {response.url}")

# Verify enrollment
is_enrolled = Enrollment.objects.filter(user=user, course=course).exists()
if is_enrolled:
    print("SUCCESS: Enrollment created.")
else:
    print("FAILURE: Enrollment not created.")

# Check course_detail context
request_detail = factory.get(f'/course/{course.id}/')
request_detail.user = user
response_detail = course_detail(request_detail, course.id)

# Note: We can't easily check the rendered HTML context without using the test client fully, 
# but we can check if no exception occurred.
print("SUCCESS: Course detail page rendered without error.")
