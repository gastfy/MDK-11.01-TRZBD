from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Div, Submit, Field, Button, Row, HTML
from .models import *
import hashlib
from .utils import log
from .validators import login_exists
from django.core.validators import FileExtensionValidator



class ReservationFilterForm(forms.Form):
    time = (
        ("Утреннее", "Утреннее"),
        ("Вечернее", "Вечернее"),
        ("Весь день", "Весь день"),
    )
    
    time = forms.ChoiceField(choices=time, label="Время", required=True)
    date = forms.DateField(label="Дата", required=True, widget=forms.DateInput(attrs={'class': 'form-control', 'type':'date', 'value': datetime.date.today().strftime("%d.%m.%Y")}), localize=True, validators=[MinValueValidator(datetime.date.today)])
    office = forms.ModelChoiceField(queryset=Office.objects.all(), required=True, label="Офис", empty_label=None)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            initial = kwargs['initial']
            self.data['date'] = initial['date'].strftime("%Y.%m.%d")
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                Div(
                    Div(
                        Field("date"),
                        css_class="row"
                    ),
                    Div(
                        Field("office"),
                        css_class="row"  
                    ),
                    css_class="box"
                ),
            ),
            Div(
                Div(
                    Div(
                        Field('time'),
                        css_class="row"
                    ),
                    style="margin-bottom: 10px;",
                    css_class="box"
                ),
                Submit(name="check", value="Показать", css_class="button is-primary")
            ),
            css_class="form-container"
            )
        )



class TimeToArchivateForm(forms.Form):
    months_to_archive = forms.IntegerField(min_value=1, required=True, label="")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("months_to_archive", css_class="column is-two-fifths"),
            Submit(name="set_time", value="Сохранить", css_class="button is-primary")
        )



class UploadFileForm(forms.Form):
    file = forms.FileField(allow_empty_file=False,  validators=[FileExtensionValidator(allowed_extensions=["json"])])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        html = """
        <div class="file has-name">
            <label class="file-label">
                <input type="file" name="file" class="file-input" required="" id="id_file">
                <span class="file-cta">
                    <span class="file-icon">
                        <i class="fas fa-upload"></i>
                    </span>
                <span class="file-label">Выберите бекап... </span>
            </span>
            <span class="file-name" name="file-name">Нет файла</span>
        </label>
        </div>
        """
        self.helper = FormHelper()
        self.helper.layout = Layout(
			Div(
                HTML(html),
                css_class="file"
            ),
            Submit(name="send", value="Отправить", css_class="button is-danger")
		)
    

class RegForm(forms.Form):
    login = forms.CharField(label="Логин", max_length=20, required=True, validators=[login_exists])
    password = forms.CharField(label="Пароль", max_length=20, required=True, widget=forms.PasswordInput)
    name = forms.CharField(label="Имя", max_length=20, required=True, empty_value=False)
    lastname = forms.CharField(label="Фамилия", max_length=20, required=True, empty_value=False)
    email = forms.EmailField(label="E-mail", required=True, empty_value=False, localize=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
				HTML("<h1 class='title is-4'>Регистрация</h1>"),
				Field('name', css_class=''),
				Field('lastname', css_class=''),
                Field('email', css_class=''),
                Field('login', css_class=''),
				Field('password', css_class=''),
				css_class="box"
			)
        )

class LoginForm(forms.Form):
    
    login = forms.CharField(label="Логин", max_length=20, required=True)
    password = forms.CharField(label="Пароль", max_length=20, required=True, widget=forms.PasswordInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
			Div(
				HTML("<h1 class='title is-4'>Авторизация</h1>"),
				Field('login', css_class=''),
				Field('password', css_class=''),
				css_class="box"
			)
		)
        
class UpdateProfile(forms.ModelForm):
    
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(), required=True, empty_value=False, min_length=5, label="Пароль", help_text="Пароль должен содержать минимум 5 символов!")
    login = forms.CharField(label="Логин", max_length=20, required=True)
    
    class Meta:
        model = User
        fields = ['name', 'lastname', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("<h1 class='title is-4'>Пользователь</h1><hr>"),
                Field('name', css_class=''),
                Field('lastname', css_class=''),
                Field('email', css_class=''),
                Field('login', css_class=''),
                Field('password', css_class=''),
                css_class="box"
            )
        )
        
    def update(self, data, id):
        hasher = hashlib.sha256(usedforsecurity=True)
        hasher.update(str(data['password']).encode())
        h_password = hasher.hexdigest()
        user = User.objects.get(id=id)
        
        if User.objects.filter(login=data['login']).exclude(id=id).exists():
            return forms.ValidationError("Логин уже существует!")
        
        user.name = data['name']
        user.lastname = data['lastname']
        user.email = data['email']
        user.login = data['login']
        user.password = h_password
        user.save()
        log(f"User with id: '{user.pk}' was updated!")


class UserFormAdd(forms.ModelForm):
    Role = (
        ("rseU", "User"),
        ("deaH", "Head"),
        ("ndmiA", "Admin")
    )
    
    role = forms.ChoiceField(choices=Role, required=True, label="Роль")
    password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=5, max_length=20, label="Пароль", help_text="Пароль должен содержать минимум 5 символов!")
    
    class Meta:
        model = User
        fields = ["name", "lastname", "email", 'is_blocked', 'login']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].validators.clear()
        self.helper = FormHelper()
        self.fields['login'].validators.append(login_exists)
        self.fields['email'].localize = True
        self.helper.layout = Layout(
            Div(
                HTML("<h1 class='title is-4'>Пользователь</h1><hr>"),
                Field('name', css_class=''),
                Field('lastname', css_class=''),
                Field('email', css_class=''),
                Div(
                    Field('login', css_class=''),
                    Div(
                        HTML('<button class="button" type="button" name="generate-login" style="margin-top: 20px;"><span class="icon is-small"><i class="fa-solid fa-rotate-right"></i></span></button>'),   
                    ),
                    css_class="field-and-button"
                ),
                Div(
                    Field('password', css_class=''),
                    Div(
                        HTML('<button class="button" type="button" name="show-password" style="margin-bottom: 2px;"><span class="icon is-small"><i class="fa-solid fa-eye"></i></span></button>'),
                        HTML('<button class="button" type="button" name="generate-password" style="margin-bottom: 2px;"><span class="icon is-small"><i class="fa-solid fa-rotate-right"></i></span></button>'),
                        css_class="buttons"
                    ),
                    css_class="field-and-button"  
                ),
                Field('role', css_class=''),
                Field('is_blocked', css_class='is_blocked'),
                css_class="box"
            )
        )
    
    def save(self, data):
        
        hasher = hashlib.sha256(usedforsecurity=True)
        hasher.update(str(data['password']).encode())
        h_password = hasher.hexdigest()
        user = User()
        user.name = data['name']
        user.lastname = data['lastname']
        user.email = data['email']
        user.login = data['login']
        user.password = h_password
        
        if Role.objects.filter(name = data['role']).exists() is False:
            role = Role()
            role.name = data['role']
            role.save()
            log(f"Role '{role}' was created!")
        
        role = Role.objects.filter(name = data['role']).first()
        user.role = role
        user.is_blocked = False
        user.save()
        log(f"User with id: '{user.pk}' was created!")
    

class UserForm(forms.ModelForm):
    
    Role = (
        ("rseU", "User"),
        ("deaH", "Head"),
        ("ndmiA", "Admin")
    )
    
    role = forms.ChoiceField(choices=Role, required=True, label="Роль")
    #wth
    password = forms.CharField(widget=forms.PasswordInput(), empty_value=[-1, -1, -1, -1, -1], required=False, min_length=5, max_length=20, label="Пароль", help_text="Пароль должен содержать минимум 5 символов!")
    
    class Meta:
        model = User
        fields = ["name", "lastname", "email", 'is_blocked', 'login']
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].validators.append(login_exists)
        self.fields['email'].localize = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("<h1 class='title is-4'>Пользователь</h1><hr>"),
                Field('name', css_class=''),
                Field('lastname', css_class=''),
                Field('email', css_class=''),
                Field('login', css_class=''),
                Field('password', css_class=''),
                Field('role', css_class=''),
                Field('is_blocked', css_class='is_blocked'),
                css_class="box"
            )
        )
    
    def save(self, data):
        
        hasher = hashlib.sha256(usedforsecurity=True)
        hasher.update(str(data['password']).encode())
        h_password = hasher.hexdigest()
        user = User()
        user.name = data['name']
        user.lastname = data['lastname']
        user.email = data['email']
        user.login = data['login']
        user.password = h_password
        
        if Role.objects.filter(name = data['role']).exists() is False:
            role = Role()
            role.name = data['role']
            role.save()
            log(f"Role '{role}' was created!")
        
        role = Role.objects.filter(name = data['role']).first()
        user.role = role
        user.is_blocked = False
        user.save()
        log(f"User with id: '{user.pk}' was created!")
    
    def update(self, data, id):
        user = User.objects.get(id=id)
        if type(data['password']) != list:
            hasher = hashlib.sha256(usedforsecurity=True)
            hasher.update(str(data['password']).encode())
            h_password = hasher.hexdigest()
            user.password = h_password
        
        if User.objects.filter(login=data['login']).exclude(id=data['user_id']).exists():
            return forms.ValidationError("Логин уже существует!")

        user.name = data['name']
        user.lastname = data['lastname']
        user.email = data['email']
        user.login = data['login']

        if Role.objects.filter(name = data['role']).exists() is False:
            role = Role()
            role.name = data['role']
            role.save()
            log(f"Role '{role}' was created!")
        
        role = Role.objects.filter(name = data['role']).first()
        user.role = role
        user.is_blocked = data['is_blocked']
        user.save()
        log(f"User with id: '{user.pk}' was updated!")
    
        
class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['address']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("<h1 class='title is-4'>Офис</h1><hr>"),
                Field('address', css_class=''),
                css_class="box"
            )
        )
    
    def save(self, data):
        office = Office()
        office.address = data['address']
        office.save()
        log(f"Office with id: '{office.pk}' was created!")
    
    def update(self, data, id):
        office = Office.objects.get(id=id)
        office.address = data['address']
        office.save()
        log(f"Office with id: '{office.pk}' was updated!")
        

class PlaceForm(forms.ModelForm):
    
    type_choice = (
        ("Стол", "Стол"),
        ("Комната", "Комната")
    )
    
    type = forms.ChoiceField(choices=type_choice, required=True, label="Тип места")
    
    class Meta:
        model = Place
        fields = ['short_name', 'office']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("<h1 class='title is-4'>Место</h1><hr>"),
                Field('short_name', css_class=''),
                Field('type', css_class=''),
                Field('office', css_class=''),
                css_class="box"
            )
        )
        
    def save(self, data):
        place = Place()
        place.short_name = data['short_name']
        place.office = data['office']
        place.save()
        log(f"Place with id: '{place.pk}' was created!")
        _type = Type()
        _type.name = data['type']
        _type.place = place
        _type.save()
        log(f"Place type with id: '{_type.pk}' was created!")
        
        
    def update(self, data, id):
        place = Place.objects.get(id=id)
        place.short_name = data['short_name']
        place.office = data['office']
        _type = Type.objects.filter(place = place).first()
        _type.name = data['type']
        _type.save()
        place.save()
        log(f"Place with id: '{place.pk}' was updated!")
        log(f"Place type with id: '{_type.pk}' was updated!")
        

class ReservationForm(forms.ModelForm):
    
    time = (
        ("Утреннее", "Утреннее"),
        ("Вечернее", "Вечернее"),
        ("Весь день", "Весь день"),
    )
    
    time = forms.ChoiceField(choices=time, label="Время бронирования", required=True)
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_blocked=False), label="Пользователь", required=True)
    date = forms.DateField(label="Дата бронирования", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type':'date'}), validators=[MinValueValidator(datetime.date.today)])
    
    class Meta:
        model = Reservation
        fields = ['type']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                HTML("<h1 class='title is-4'>Бронирование</h1><hr>"),
                Field('user', css_class=''),
                Field('time', css_class=''),
                Field('status', css_class=''),
                Field('type', css_class=''),
                Field('date', css_class=''),
                css_class="box"
            )
        )
    
    
    def save(self, data):
        rs = Reservation()
        rs.user = data['user']
        
        if Time.objects.filter(time = data['time']).exists() is False:
            time = Time()
            time.time = str(data['time'])
            time.save()

        time = Time.objects.filter(time = str(data['time'])).first()
        
        rs.time = time
        
        if Status.objects.filter(status = "Забронировано").exists() is False:
            status = Status()
            status.status = "Забронировано"
            status.save()
            log(f"Status '{status.status}' was created!")
        
        if Status.objects.filter(status = "Завершено").exists() is False:
            status = Status()
            status.status = "Завершено"
            status.save()
            log(f"Status '{status.status}' was created!")
            
        if Status.objects.filter(status = "Отменено").exists() is False:
            status = Status()
            status.status = "Отменено"
            status.save()
            log(f"Status '{status.status}' was created!")
        
        _status = Status.objects.filter(status = "Забронировано").first()
        rs.status = _status
        rs.type = data['type']
        rs.date = data['date']
        rs.save()
        log(f"Reservation with id: '{rs.pk}' was created!")
        
    def update(self, data, id):
        rs = Reservation.objects.get(id=id)
        rs.user = data['user']
        if Time.objects.filter(time = data['time']).exists():
            time = Time()
            time.time = data['time']
            time.save()

        time = Time.objects.filter(time = data['time']).first()
        
        rs.time = time
        if Status.objects.filter(status = "Забронировано").exists() is False:
            status = Status()
            status.status = "Забронировано"
            status.save()
            log(f"Status '{status.status}' was created!")
        
        if Status.objects.filter(status = "Завершено").exists() is False:
            status = Status()
            status.status = "Завершено"
            status.save()
            log(f"Status '{status.status}' was created!")
            
        if Status.objects.filter(status = "Отменено").exists() is False:
            status = Status()
            status.status = "Отменено"
            status.save()
            log(f"Status '{status.status}' was created!")
        
        _status = Status.objects.filter(status = "Отменено").first()
        rs.type = data['type']
        rs.date = data['date']
        rs.save()
        log(f"Reservation with id: '{rs.pk}' was updated!")