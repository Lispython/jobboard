# -*- coding:  utf-8 -*-

cats_list = (
    u"Design",
    u"Programming",
    u"Business/Exec",
    u"Miscellaneous",
    u"Copywriter",
    u"iPhone Developer",
    u"Customer Service/Support"
    )


cats = [(i, x) for i, x in enumerate(cats_list)]

jobs_list = (
    u"full-time",
    u"freelance",
    u"part-time", 
    )

job_types =  [(i, x) for i, x in enumerate(jobs_list)]
