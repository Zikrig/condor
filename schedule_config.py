from datetime import time

# Конфигурация расписания
SCHEDULE_CONFIG = [
    {
        'schedule': {
            'hour': 9,
            'minute': 50,
            'day_of_week': '*', # 'mon-fri'  # Понедельник-пятница
        },
        'task_type': 'theme',
        'params': {'theme': 'content'}
    },
    # {
    #     'schedule': {
    #         'hour': 11,
    #         'minute': 41,
    #         'day_of_week': '1,3,5' # вторник, четверг, суббота
    #     },
    #     'task_type': 'theme',
    #     'params': {'theme': 'content'}
    # },
    {
        'schedule': {
            'hour': 16,
            'minute': 0,
            'day_of_week': '*'  # Каждый день
        },
        'task_type': 'post_id',
        'params': {'post_id': 186}
    }
] 