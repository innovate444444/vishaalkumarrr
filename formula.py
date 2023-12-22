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
detected_cracks = [
    "frames/frame_00000090.png",
    "frames/frame_00000100.png",
    "frames/frame_00000235.png",
    # Add more paths as needed
]

# Extracting last two digits from each path and storing them in det_t list
det_t = [int(path[-7:-4]) for path in detected_cracks]

print(det_t)
  # Displaying the extracted digits


for i in det_t:
    ver_h,ver_t,hr_h,hr_t=20,180,1,5
    l1=formula(ver_h,ver_t,hr_h,hr_t,i)

    print(l1)