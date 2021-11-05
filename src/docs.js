/**
 * @typedef {number} integer
 * 
 * @typedef {object} Assignment
 * @property {LessonSubject} subject
 * @property {string} complete_before
 * @property {?string} description
 * @property {string} title
 * @property {boolean} is_important
 * @property {boolean} archived
 * @property {Group} group
 * @property {Subgroup} subgroup
 * @property {integer} id
 * 
 * @typedef {object} Body_update_student_assignment_students__student_id__assignments__student_assignment_id__patch
 * @property {boolean} done
 * 
 * @typedef {string} Building
 * Перечисление корпусов университета
 * 
 * @typedef {object} ClassRoom
 * Модель, описывающая аудиторию
 * @property {integer} number - Номер аудитории
 * @property {Building} building - Корпус университета, в котором находится аудитория
 * @property {integer} id
 * 
 * @typedef {object} Group
 * Модель, описывающая группу
 * @property {string} name - Название группы
 * @property {integer} id
 * 
 * @typedef {object} HTTPValidationError
 * @property {?array} detail
 * 
 * @typedef {object} Lesson
 * Модель, описывающая пару
 * @property {LessonSubject} subject - Предмет, по которому проходит пара
 * @property {Teacher} teacher - Преподаватель, который ведет пару
 * @property {?ClassRoom} classroom - Аудитория, в которой проходит пара
 * @property {Group} group - Группа, у которой проходит пара
 * @property {Subgroup} subgroup - Подгруппа, у которой проходит пара
 * @property {LessonKind} kind - Тип занятия
 * @property {WeekDay} day - День недели, в который проходит пара, в виде перечисления
 * @property {Parity} parity - Четность недели, в которую проходит пара
 * @property {string} time - Время прохождения пары
 * @property {integer} id
 * 
 * @typedef {string} LessonKind
 * Перечисление типов пары
 * 
 * @typedef {object} LessonSubject
 * Модель, описывающая предмет
 * @property {string} name - Название предмета
 * @property {integer} id
 * 
 * @typedef {string} Parity
 * Перечисление вариантов четности пары (числитель, знаменатель или всегда)
 * 
 * @typedef {object} Student
 * @property {integer} telegram_id
 * @property {Subgroup} subgroup
 * @property {Group} group
 * 
 * @typedef {object} StudentAssignment
 * @property {Assignment} assignment
 * @property {Student} student
 * @property {boolean} done
 * @property {integer} id
 * 
 * @typedef {object} StudentCreate
 * @property {integer} telegram_id
 * @property {Subgroup} subgroup
 * @property {string} group_name
 * 
 * @typedef {object} StudentUpdate
 * @property {string} group_name
 * @property {Subgroup} subgroup
 * 
 * @typedef {string} Subgroup
 * Перечисления подгрупп
 * 
 * @typedef {object} Subject
 * Модель, описывающая предмет
 * @property {string} name - Название предмета
 * @property {integer} id
 * @property {?array} useful_links
 * 
 * @typedef {object} Teacher
 * Модель, описывающая преподавателя
 * @property {string} first_name - Имя преподавателя
 * @property {string} second_name - Фамилия преподавателя
 * @property {string} middle_name - Отчество преподавателя
 * @property {integer} id
 * 
 * @typedef {object} UsefulLink
 * @property {string} link
 * @property {?string} description
 * @property {integer} id
 * 
 * @typedef {object} ValidationError
 * @property {array} loc
 * @property {string} msg
 * @property {string} type
 * 
 * @typedef {string} WeekDay
 * Перечисления дней недели
 * 
 */
