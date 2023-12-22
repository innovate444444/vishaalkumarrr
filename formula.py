
def formula(ver_h, ver_t, hr_h, hr_t, det_t):
    no_of_units = det_t/(ver_t+hr_t)
    hr_comp = int(str(no_of_units)[0])
    ver_comp = no_of_units-hr_comp
    hr_tr = hr_comp*hr_h
    ver_tr = ver_comp*ver_h
    if hr_tr%2 !=0:
        depth = ver_h-ver_tr
    else:
        depth = ver_tr
    
    return (hr_tr, depth)

det=[700,908,2098,3000]
for i in det:
    ver_h,ver_t,hr_h,hr_t=20,180,1,5
    l1=formula(ver_h,ver_t,hr_h,hr_t,i)

    print(l1)