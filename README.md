## ⚙️ Setup & Run

```bash
# Clone repo
git clone https://github.com/nPhuongNguyen/django-ecom.git

# Create virtual env
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
python manage.py runserver

# Run task
celery -A ecom worker --loglevel=info --pool=solo -Q celery,woker-push-task
