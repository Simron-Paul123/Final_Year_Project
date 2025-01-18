import os
from django.conf import settings
from django.shortcuts import render,HttpResponse,redirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

#import resume_parsing
from .resume_parsing import extract_education, extract_email, extract_mobile_number, extract_name, extract_skills, extract_text_from_pdf
from .models import Category, CustomUser, Job

# Create your views here.
@login_required
def trypage(request):
    user = request.user  # Get the logged-in user
    # Get the user's skills as a set (split by comma, convert to lowercase, and strip any extra spaces)
    user_skills = {skill.strip().lower() for skill in user.skills.split(',')} if hasattr(user, 'skills') and user.skills else set()
    print(f"user skills: {user_skills}")  # Debugging

    # Fetch all jobs
    jobs = Job.objects.all()

    matched_jobs = []

    for job in jobs:
        # Extract the required skills for the job (split by comma, convert to lowercase, and strip any spaces)
        required_skills = {skill.strip().lower() for skill in job.skill.split(',')} if job.skill else set()
        print(f"required skills: {required_skills}")  # Debugging

        # Find the intersection of user skills and required skills
        matched_skills = user_skills.intersection(required_skills)
        print(f"matched skills: {matched_skills}")  # Debugging

        # Match percentage condition (50% or more match)
        if len(required_skills) > 0 and (len(matched_skills) / len(required_skills)) >= 0.5:
            job.skills_list = job.skill.split(',')
            matched_jobs.append(job)

    # Render only matched jobs to the template
    return render(request, 'try.html', {'jobs': matched_jobs})

@login_required(login_url='login')
def HomePage(request):
    return render (request,'job_seeker.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.usertype == 'recruiter' and not user.is_approved:
                return HttpResponse("Your account is awaiting for admin approval.")
            
            login(request, user)
            
            if user.usertype == 'recruiter':
                return redirect('company')  # Update this with your recruiter dashboard URL
            
            elif user.usertype == 'job_seeker':
                # Check if CV is provided
                if user.cv:
                    return redirect('job_seeker')  # Update this with your job seeker dashboard URL
                else:
                    return redirect('prediction')  # Redirect to a page prompting them to upload CV
            
        else:
            return HttpResponse("Username or Password is incorrect!")
    
    return render(request, 'user_reg.html')

def register_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        usertype = request.POST.get('usertype')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not the same!")
        if CustomUser.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists!")
        if CustomUser.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")
        if usertype not in ['recruiter', 'job_seeker']:
            return HttpResponse("Invalid user type!")

        # Create the user
        is_approved = usertype == 'job_seeker'  # Job seekers are auto-approved
        my_user = CustomUser.objects.create_user(username=uname, email=email, password=pass1, usertype=usertype, is_approved=is_approved)
        my_user.save()
        return redirect('login')
    return render(request, 'user_reg.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def job_seeker(request):
    jobs = Job.objects.all()  # Fetch all job entries from the Job model
    categories = Category.objects.all()  # Fetch all category entries from the Category model
    return render(request, 'job_seeker.html', {'jobs': jobs, 'categories': categories})

def all_jobs(request):
    jobs = Job.objects.all()
    for job in jobs:
        job.skills_list = job.skill.split(',')  # Add a skills_list attribute
    return render(request, 'all_jobs.html', {'jobs': jobs})

@login_required(login_url='login')
def company(request):
    return render(request, 'company.html')


@login_required(login_url='login')
def user_dashboard(request):
    user = request.user  # Get the logged-in user
    recommended_jobs = []  # To store the recommended jobs
    success_message = None  # To store a success message

    if request.method == "POST":
        try:
            # Handle profile picture upload
            if request.FILES.get('profile_pic'):
                profile_pic = request.FILES['profile_pic']

                # Create a unique filename to avoid overwrites
                file_extension = os.path.splitext(profile_pic.name)[1]
                unique_filename = f"{user.username}_{user.id}{file_extension}"
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profile_pics'))
                filename = fs.save(unique_filename, profile_pic)
                user.profile_pic = f"profile_pics/{filename}"

            # Handle other form fields
            user.phone_no = request.POST.get('phone', user.phone_no)
            user.education = request.POST.get('education', user.education)
            user.skills = request.POST.get('skills', user.skills)

            # Save the user profile
            user.save()

            # Set success message
            success_message = "Your profile has been updated successfully!"

        except Exception as e:
            return render(request, 'user_dashboard.html', {
                'user': user,
                'error': f"An error occurred: {e}",
            })
    user_skills = set(user.skills.lower().split(',')) if user.skills else set()

    if 'recommended' in request.GET:
        user = request.user  # Get the logged-in user
    # Get the user's skills as a set (split by comma, convert to lowercase, and strip any extra spaces)
        user_skills = {skill.strip().lower() for skill in user.skills.split(',')} if hasattr(user, 'skills') and user.skills else set()
        print(f"user skills: {user_skills}")  # Debugging

    # Fetch all jobs
        jobs = Job.objects.all()

        matched_jobs = []

        for job in jobs:
            # Extract the required skills for the job (split by comma, convert to lowercase, and strip any spaces)
            required_skills = {skill.strip().lower() for skill in job.skill.split(',')} if job.skill else set()
            print(f"required skills: {required_skills}")  # Debugging

            # Find the intersection of user skills and required skills
            matched_skills = user_skills.intersection(required_skills)
            print(f"matched skills: {matched_skills}")  # Debugging

            # Match percentage condition (50% or more match)
            if len(required_skills) > 0 and (len(matched_skills) / len(required_skills)) >= 0.5:
                job.skills_list = job.skill.split(',')
                matched_jobs.append(job)

    # Render only matched jobs to the template
        return render(request, 'user_dashboard.html', {'jobs': matched_jobs})
    context = {
        'name': user.username,
        'email': user.email,
        'phone': user.phone_no,
        'education': user.education,
        'skills': user.skills,
        'profile_pic': user.profile_pic,
        'success_message': success_message,  # Pass success message to the template
    }

    return render(request, 'user_dashboard.html', context)
@login_required(login_url='login')
def prediction(request):
    if request.method == 'POST' and request.FILES.get('resume'):
        resume = request.FILES['resume']
        fs = FileSystemStorage(location='media/cv/')  # Save in media/cv/
        filename = fs.save(resume.name, resume)
        uploaded_file_url = fs.url(filename)
        
        # Update the user model
        user = request.user
        user.cv = f"cv/{filename}"  # Relative path to the file
        user.save()
        pdf_path = user.cv.path
        extracted_text = extract_text_from_pdf(pdf_path)
        user.username = extract_name(extracted_text)
        user.email = user.email #extract_email(extracted_text) or 
        user.phone_no = extract_mobile_number(extracted_text)
        skills_list = ['Python', 'Data Analysis', 'Machine Learning','SpringBoot', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau',
    'Java', 'C++', 'JavaScript', 'HTML', 'CSS', 'React', 'Angular', 'Node.js', 'MongoDB', 'Express.js', 'Git',
    'Research', 'Statistics', 'Quantitative Analysis', 'Qualitative Analysis', 'SPSS', 'R', 'Data Visualization', 'Matplotlib',
    'Seaborn', 'Plotly', 'Pandas', 'Numpy', 'Scikit-learn', 'TensorFlow', 'Keras', 'PyTorch', 'NLTK', 'Text Mining',
    'Natural Language Processing', 'Computer Vision', 'Image Processing', 'OCR', 'Speech Recognition', 'Recommendation Systems',
    'Collaborative Filtering', 'Content-Based Filtering', 'Reinforcement Learning', 'Neural Networks', 'Convolutional Neural Networks',
    'Recurrent Neural Networks', 'Generative Adversarial Networks', 'XGBoost', 'Random Forest', 'Decision Trees', 'Support Vector Machines',
    'Linear Regression', 'Logistic Regression', 'K-Means Clustering', 'Hierarchical Clustering', 'DBSCAN', 'Association Rule Learning',
    'Apache Hadoop', 'Apache Spark', 'MapReduce', 'Hive', 'HBase', 'Apache Kafka', 'Data Warehousing', 'ETL', 'Big Data Analytics',
    'Cloud Computing', 'Amazon Web Services (AWS)', 'Microsoft Azure', 'Google Cloud Platform (GCP)', 'Docker', 'Kubernetes', 'Linux',
    'Shell Scripting', 'Cybersecurity', 'Network Security', 'Penetration Testing', 'Firewalls', 'Encryption', 'Malware Analysis',
    'Digital Forensics', 'CI/CD', 'DevOps', 'Agile Methodology', 'Scrum', 'Kanban', 'Continuous Integration', 'Continuous Deployment',
    'Software Development', 'Web Development', 'Mobile Development', 'Backend Development', 'Frontend Development', 'Full-Stack Development',
    'UI/UX Design', 'Responsive Design', 'Wireframing', 'Prototyping', 'User Testing', 'Adobe Creative Suite', 'Photoshop', 'Illustrator',
    'InDesign', 'Figma', 'Sketch', 'Zeplin', 'InVision', 'Product Management', 'Market Research', 'Customer Development', 'Lean Startup',
    'Business Development', 'Sales', 'Marketing', 'Content Marketing', 'Social Media Marketing', 'Email Marketing', 'SEO', 'SEM', 'PPC',
    'Google Analytics', 'Facebook Ads', 'LinkedIn Ads', 'Lead Generation', 'Customer Relationship Management (CRM)', 'Salesforce',
    'HubSpot', 'Zendesk', 'Intercom', 'Customer Support', 'Technical Support', 'Troubleshooting', 'Ticketing Systems', 'ServiceNow',
    'ITIL', 'Quality Assurance', 'Manual Testing', 'Automated Testing', 'Selenium', 'JUnit', 'Load Testing', 'Performance Testing',
    'Regression Testing', 'Black Box Testing', 'White Box Testing', 'API Testing', 'Mobile Testing', 'Usability Testing', 'Accessibility Testing',
    'Cross-Browser Testing', 'Agile Testing', 'User Acceptance Testing', 'Software Documentation', 'Technical Writing', 'Copywriting',
    'Editing', 'Proofreading', 'Content Management Systems (CMS)', 'WordPress', 'Joomla', 'Drupal', 'Magento', 'Shopify', 'E-commerce',
    'Payment Gateways', 'Inventory Management', 'Supply Chain Management', 'Logistics', 'Procurement', 'ERP Systems', 'SAP', 'Oracle',
    'Microsoft Dynamics', 'Tableau', 'Power BI', 'QlikView', 'Looker', 'Data Warehousing', 'ETL', 'Data Engineering', 'Data Governance',
    'Data Quality', 'Master Data Management', 'Predictive Analytics', 'Prescriptive Analytics', 'Descriptive Analytics', 'Business Intelligence',
    'Dashboarding', 'Reporting', 'Data Mining', 'Web Scraping', 'API Integration', 'RESTful APIs', 'GraphQL', 'SOAP', 'Microservices',
    'Serverless Architecture', 'Lambda Functions', 'Event-Driven Architecture', 'Message Queues', 'GraphQL', 'Socket.io', 'WebSockets'
'Ruby', 'Ruby on Rails', 'PHP', 'Symfony', 'Laravel', 'CakePHP', 'Zend Framework', 'ASP.NET', 'C#', 'VB.NET', 'ASP.NET MVC', 'Entity Framework',
    'Spring', 'Hibernate', 'Struts', 'Kotlin', 'Swift', 'Objective-C', 'iOS Development', 'Android Development', 'Flutter', 'React Native', 'Ionic',
    'Mobile UI/UX Design', 'Material Design', 'SwiftUI', 'RxJava', 'RxSwift', 'Django', 'Flask', 'FastAPI', 'Falcon', 'Tornado', 'WebSockets',
    'GraphQL', 'RESTful Web Services', 'SOAP', 'Microservices Architecture', 'Serverless Computing', 'AWS Lambda', 'Google Cloud Functions',
    'Azure Functions', 'Server Administration', 'System Administration', 'Network Administration', 'Database Administration', 'MySQL', 'PostgreSQL',
    'SQLite', 'Microsoft SQL Server', 'Oracle Database', 'NoSQL', 'MongoDB', 'Cassandra', 'Redis', 'Elasticsearch', 'Firebase', 'Google Analytics',
    'Google Tag Manager', 'Adobe Analytics', 'Marketing Automation', 'Customer Data Platforms', 'Segment', 'Salesforce Marketing Cloud', 'HubSpot CRM',
    'Zapier', 'IFTTT', 'Workflow Automation', 'Robotic Process Automation (RPA)', 'UI Automation', 'Natural Language Generation (NLG)',
    'Virtual Reality (VR)', 'Augmented Reality (AR)', 'Mixed Reality (MR)', 'Unity', 'Unreal Engine', '3D Modeling', 'Animation', 'Motion Graphics',
    'Game Design', 'Game Development', 'Level Design', 'Unity3D', 'Unreal Engine 4', 'Blender', 'Maya', 'Adobe After Effects', 'Adobe Premiere Pro',
    'Final Cut Pro', 'Video Editing', 'Audio Editing', 'Sound Design', 'Music Production', 'Digital Marketing', 'Content Strategy', 'Conversion Rate Optimization (CRO)',
    'A/B Testing', 'Customer Experience (CX)', 'User Experience (UX)', 'User Interface (UI)', 'Persona Development', 'User Journey Mapping', 'Information Architecture (IA)',
    'Wireframing', 'Prototyping', 'Usability Testing', 'Accessibility Compliance', 'Internationalization (I18n)', 'Localization (L10n)', 'Voice User Interface (VUI)',
    'Chatbots', 'Natural Language Understanding (NLU)', 'Speech Synthesis', 'Emotion Detection', 'Sentiment Analysis', 'Image Recognition', 'Object Detection',
    'Facial Recognition', 'Gesture Recognition', 'Document Recognition', 'Fraud Detection', 'Cyber Threat Intelligence', 'Security Information and Event Management (SIEM)',
    'Vulnerability Assessment', 'Incident Response', 'Forensic Analysis', 'Security Operations Center (SOC)', 'Identity and Access Management (IAM)', 'Single Sign-On (SSO)',
    'Multi-Factor Authentication (MFA)', 'Blockchain', 'Cryptocurrency', 'Decentralized Finance (DeFi)', 'Smart Contracts', 'Web3', 'Non-Fungible Tokens (NFTs)']

        user.skills = ", ".join(extract_skills(extracted_text,skills_list))

        education_keywords = ['Computer Science', 'Information Technology', 'Software Engineering', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
        'Chemical Engineering', 'Biomedical Engineering', 'Aerospace Engineering', 'Nuclear Engineering', 'Industrial Engineering', 'Systems Engineering',
        'Environmental Engineering', 'Petroleum Engineering', 'Geological Engineering', 'Marine Engineering', 'Robotics Engineering', 'Biotechnology',
        'Biochemistry', 'Microbiology', 'Genetics', 'Molecular Biology', 'Bioinformatics', 'Neuroscience', 'Biophysics', 'Biostatistics', 'Pharmacology',
        'Physiology', 'Anatomy', 'Pathology', 'Immunology', 'Epidemiology', 'Public Health', 'Health Administration', 'Nursing', 'Medicine', 'Dentistry',
        'Pharmacy', 'Veterinary Medicine', 'Medical Technology', 'Radiography', 'Physical Therapy', 'Occupational Therapy', 'Speech Therapy', 'Nutrition',
        'Sports Science', 'Kinesiology', 'Exercise Physiology', 'Sports Medicine', 'Rehabilitation Science', 'Psychology', 'Counseling', 'Social Work',
        'Sociology', 'Anthropology', 'Criminal Justice', 'Political Science', 'International Relations', 'Economics', 'Finance', 'Accounting', 'Business Administration',
         'Marketing', 'Entrepreneurship', 'Hospitality Management', 'Tourism Management', 'Supply Chain Management', 'Logistics Management',
        'Operations Management', 'Human Resource Management', 'Organizational Behavior', 'Project Management', 'Quality Management', 'Risk Management',
        'Strategic Management', 'Public Administration', 'Urban Planning', 'Architecture', 'Interior Design', 'Landscape Architecture', 'Fine Arts',
        'Visual Arts', 'Graphic Design', 'Fashion Design', 'Industrial Design', 'Product Design', 'Animation', 'Film Studies', 'Media Studies',
        'Communication Studies', 'Journalism', 'Broadcasting', 'Creative Writing', 'English Literature', 'Linguistics', 'Translation Studies',
        'Foreign Languages', 'Modern Languages', 'Classical Studies', 'History', 'Archaeology', 'Philosophy', 'Theology', 'Religious Studies',
        'Ethics', 'Early Childhood Education', 'Elementary Education', 'Secondary Education', 'Special Education', 'Higher Education',
        'Adult Education', 'Distance Education', 'Online Education', 'Instructional Design', 'Curriculum Development'
        'Library Science', 'Information Science', 'Computer Engineering', 'Software Development', 'Cybersecurity', 'Information Security',
        'Network Engineering', 'Data Science', 'Data Analytics', 'Business Analytics', 'Operations Research', 'Decision Sciences',
        'Human-Computer Interaction', 'User Experience Design', 'User Interface Design', 'Digital Marketing', 'Content Strategy',
        'Brand Management', 'Public Relations', 'Corporate Communications', 'Media Production', 'Digital Media',
        'Mobile App Development', 'Game Development', 'Virtual Reality', 'Augmented Reality', 'Blockchain Technology', 'Cryptocurrency',
        'Digital Forensics', 'Forensic Science', 'Criminalistics', 'Crime Scene Investigation', 'Emergency Management', 'Fire Science',
        'Environmental Science', 'Climate Science', 'Meteorology', 'Geography', 'Geomatics', 'Remote Sensing', 'Geoinformatics',
        'Cartography', 'GIS (Geographic Information Systems)', 'Environmental Management', 'Sustainability Studies', 'Renewable Energy',
        'Green Technology', 'Ecology', 'Conservation Biology', 'Wildlife Biology', 'Zoology']

        user.education= ", ".join(extract_education(extracted_text,education_keywords))
        user.save()  # Save all extracted details to the database
        print(f"File saved at: {uploaded_file_url}")  # Debugging
        messages.success(request, "Your resume has been uploaded successfully!")
        return redirect('user_dashboard')
    return render(request, 'prediction.html')


