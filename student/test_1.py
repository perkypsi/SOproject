import os

from social_student_сouncil.student.models import Event

files = set()

# for root, dir, filenames in os.walk("C:\\Projects\\so_network\\social_student_сouncil\\student"):
#     for filename in filenames:
#         try:
#             with open(f"{root}\\{filename}", mode='r', encoding="utf8") as file:
#                 file_data = file.read()
#             file_data = file_data.replace('комитет', 'комитет')
#             file_data = file_data.replace('комитеты', 'комитеты')
#             file_data = file_data.replace('Комитет', 'Комитет')
#             file_data = file_data.replace('Комитеты', 'Комитеты')
#             with open(f"{root}\\{filename}", mode='w', encoding="utf8") as file:
#                 file.write(file_data)
#         except Exception:
#             continue


for root, dir, filenames in os.walk("C:\\Projects\\so_network\\social_student_сouncil\\student"):
    for filename in filenames:
        try:
            with open(f"{root}\\{filename}", encoding="utf8") as file:
                for line in file.readlines():
                    if 'link_telegram' in line:
                        files.add(filename)
        except Exception:
            continue



print(files)


# import math
#
# Na = 6.022 * 10**23
# h = 6.26607015 * 10**(-34)
#
# d = 3.9 * 10**(-9)
# V = 4/3 * math.pi * (d/2)**3
#
# print(f"Объем шара = {V:.3}")
#
# dens_pbs = 7500  # кг/м3
# dens_cds = 4820  # кг/м3
#
# mr_pbs = 239.28  # г/моль
# mr_cds = 144.46  # г/моль
#
# n_pbs = (dens_pbs * V) * 1000 / mr_pbs
# n_cds = (dens_cds * V) * 1000 / mr_cds
#
# print(f"Масса CdS = {dens_pbs * V:.3}")
# print(f"Масса PbS = {dens_cds * V:.3}")
#
# N_cds = n_cds * Na
# N_pbs = n_pbs * Na
#
# print(f"Молекул в PbS = {N_pbs:.2f}")
# print(f"Молекул в CdS = {N_cds:.2f}")
#
# m_free_electron = 9.1093837015 * 10**(-31)
# me = 0.2 * m_free_electron
# mh = 1.4 * m_free_electron
#
# meff_1 = (1 / me) + (1 / mh)
# meff = meff_1**(-1)
#
# print(f"m_eff = {meff:0.4} кг")
#
# dEg = ((2 * math.pi * h**2) / (meff * d**2)) / (1.602176634*10**(-19))
# print(f"dE = {((2 * math.pi * h**2) / (meff * d**2)):.4} дж")
# print(f"dE = {dEg:.3f} еВ")

from docxtpl import DocxTemplate
import datetime as dt

doc = DocxTemplate("../media/templates/project_map_template.docx")
event = Event.objects.all[0]
context = {
    'event': event
}
doc.render(context)
doc.save("res.docx")