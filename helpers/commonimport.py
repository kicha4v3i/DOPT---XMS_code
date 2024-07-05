from django.http import JsonResponse,HttpResponse,Http404
from django.conf import settings
import json
from django.conf.urls.static import static
from django.template.loader import get_template
from PIL import Image
import base64
from django.db.models import Q,Count
from datetime import date, timedelta,datetime
from django.utils import timezone
import io 
import xlsxwriter
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
from notifications.signals import notify
from notifications.models import Notification
from django.core.files.storage import FileSystemStorage
from django.views.generic import ListView, DetailView, View
import os
import mimetypes
from urllib.parse import unquote




