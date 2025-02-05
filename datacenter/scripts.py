from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from datacenter.models import Chastisement, Schoolkid, Mark, Lesson, Subject, Commendation
import datetime


def get_full_name(full_name):
    try:
        return Schoolkid.objects.get(full_name=full_name)
    except ObjectDoesNotExist:
        print(f"Ошибка: Ученик с именем '{full_name}' не найден.")
    except MultipleObjectsReturned:
        print(f"Ошибка: Найдено несколько учеников с именем '{full_name}', уточните запрос.")
    return None


def remove_chastisements(full_name):
    kid_id = get_full_name(full_name)
    chastisements = Chastisement.objects.filter(schoolkid=kid_id)
    chastisements.delete()
    return f"Удалено {len(chastisements)} замечаний."


def create_commendation(full_name,subject,group_letter):
    kid_id = get_full_name(full_name)
    year_of_study = kid_id.year_of_study
    subject = Subject.objects.filter(title=subject,year_of_study=year_of_study).first()
    lesson = Lesson.objects.filter(
        subject=subject,
        year_of_study = year_of_study,
        group_letter = group_letter,
    ).first()
    teacher = lesson.teacher
    today = datetime.date.today()
    commendation = Commendation.objects.create(
        text="Хвалю!",
        created=today,  # Указываем текущую дату
        schoolkid=kid_id,
        subject=subject,  # Используем предмет из урока
        teacher=teacher  # Используем учителя из урока
    )

    return f"Добавлена похвала."


def fix_marks(full_name):
    kid_id = get_full_name(full_name)
    childs = Mark.objects.filter(schoolkid=kid_id, points__lt=4)
    for child in childs:
        child.points = 5
        child.save()
    return f"Оценки исправлены."