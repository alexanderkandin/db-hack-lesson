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
    if not kid_id:
        return f"Ошибка: ученик '{full_name}' не найден."

    chastisements = Chastisement.objects.filter(schoolkid=kid_id)
    count, _ = chastisements.delete()
    return f"Удалено {count} замечаний."


def create_commendation(full_name,subject,group_letter):
    kid_id = get_full_name(full_name)
    if not kid_id:
        return f"Ошибка: ученик '{full_name}' не найден."

    year_of_study = kid_id.year_of_study
    subject_obj = Subject.objects.filter(title=subject,year_of_study=year_of_study).first()

    if not subject_obj:
        return f"Ошибка: предмет '{subject}' не найден для {year_of_study} класса {group_letter}."
    lesson = Lesson.objects.filter(
        subject=subject_obj,
        year_of_study = year_of_study,
        group_letter = group_letter,
    ).first()


    if not lesson:
        return f"Ошибка: урок по предмету '{subject}' для {year_of_study}{group_letter} не найден."

    teacher = lesson.teacher
    today = datetime.date.today()
    commendation = Commendation.objects.create(
        text="Хвалю!",
        created=today,  # Указываем текущую дату
        schoolkid=kid_id,
        subject=subject_obj,  # Используем предмет из урока
        teacher=teacher  # Используем учителя из урока
    )

    return f"Добавлена похвала."


def fix_marks(full_name):
    kid_id = get_full_name(full_name)
    if not kid_id:
        return f"Ошибка: ученик '{full_name}' не найден."

    Mark.objects.filter(schoolkid=kid_id, points__lt=4).update(points=5)

    return f"Оценки исправлены."