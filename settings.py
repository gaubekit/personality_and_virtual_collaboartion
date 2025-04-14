from os import environ

SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1, participation_fee=0)
SESSION_CONFIGS = [dict(name='PersonalityBehaviorVirtualCollaboration', num_demo_participants=3,
                        app_sequence=['App01',  # Intro -> Block a, b, c
                                      'App02',  # Treatment -> Block d
                                      'App03',  # Questionnaires -> Block e
                                      'App04'  # Outro -> Block d
                                      ])]
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False
DEMO_PAGE_INTRO_HTML = ''
PARTICIPANT_FIELDS = ['consent',
                      'svo_self',
                      'svo_to_other',
                      'svo_other',
                      'vm_pref_achievement',
                      'vm_pref_dominance',
                      'vm_pref_face',
                      'vm_pref_rules',
                      'vm_pref_concern',
                      'vm_pref_tolerance',
                      'wait_page_arrival',
                      'single_player',
                      'wlg_own_choice',
                      'wlg_min_choice',
                      'wlg_payoff',
                      'attention_fail',
                      'attention_fail_cost',
                      'additional_payoff',
                      'fixed_payoff',
                      'total_payoff',
                      'final_payoff'
                      ]

SESSION_FIELDS = ['vm_goal_labels']
ROOMS = [
    dict(
        name='PersonalityBehavior',
        display_name='Personality and Behavior in virtual Collaboration'
    )]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

SECRET_KEY = 'blahblah'
OTREE_REST_KEY = 'otreehapsserverrest3'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
