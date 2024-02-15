from datetime import datetime

#            <A HREF="https://app.sketchup.com/app?hl=en" ADD_DATE="1667000298" TAGS="bookmarks bar, woodworking, import-2023-05-07" NOTES="">SketchUp

class Bookmark:
    def __init__ (self, catagory, sub_catagory, line, indent):
        self.catagory = catagory
        self.sub_catagory = sub_catagory
        self.line = line
        self.indent = indent

    @property
    def bookmark (self):
        find_location = line.find ("<A")
        if find_location > 0:
            address_line = line [find_location + 9:-1:]
            address_end = address_line.find ('"')
            address = address_line[:address_end:]
            return address
        else:
            return ""
    
    @property
    def bm_date (self):
        find_location = line.find ('ADD_DATE="')
        if find_location > 0:
            date_line = self.line [find_location+10:find_location+20:]
            date_time = datetime.fromtimestamp( int(date_line) ) 
            # print (f'{date_time:%d-%m-%Y }')
            # return f'{date_time:%d-%m-%Y }'
            return f'{date_line}'
        else:
            return ""
    
    @property
    def name (self):
        find_location = line.find ('">')
        if find_location > 0:
            name = self.line [find_location+2:-1:]
            return name
        else:
            return ""

    @property
    def notes (self):
        find_location = line.find ('NOTES="')
        if find_location > 0:
            note_line = line [find_location + 7:-1:]
            note_end = note_line.find ('"')
            note = note_line[:note_end:]
            return note
        else:
            return ""

    @property
    def tags (self):
        find_location = line.find ('TAGS="')
        if find_location > 0:
            tag_line = line [find_location + 6:-1:]
            tag_end = tag_line.find ('" NOTES')
            all_tags = tag_line[:tag_end:]
            tags_list = all_tags.split(",")
            tags=[]
            for t in tags_list:
                tags.append(t.strip())

            # print (f'{tag_line = } {tags = } ')
            return tags
        else:
            return ""

    def __repr__(self) -> str:
        date_time = datetime.fromtimestamp( int(self.bm_date) ) 
        return f"{self.name} \nwith {self.catagory} / {self.sub_catagory} --> \t{self.bookmark} on {date_time:%d-%m-%Y} \nNotes: {self.notes} with tags {self.tags}\n\n"
        # return f"{self.tags}"
    
    def __str__ (self) -> str:
        spaces = " "*self.indent
        return f'{spaces}<DT><A HREF"{self.bookmark}" TAGS="{self.tags}" ADD_DATE={self.bm_date}">{self.name}</A>\n'
    
if __name__ == "__main__":

    catagory = ""
    sub_cat = ""

    with open ("/home/michael/Desktop/super_temp/ninja.txt", "r") as file:
        output_lines = []
        tag_list = []
        indent = 0
        for line in file:
            find_location = line.find ("<H3>")
            # print (f'{find_location = }')
            if find_location == 4:
                catagory = line[8:-1:]
                indent = 4
            
            if find_location == 8:
                sub_cat = line[12:-1:]
                indent = 8

                # cat = Bookmark (line)
                # print (f'{line = } {find_location = }')

                # print (f'{catagory = }  {sub_cat = }')
            
            find_location = line.find ("<A")
            if find_location > 0:
                cat = Bookmark (catagory, sub_cat, line, indent)
                # print (f'{str(cat)}')
                output_lines.append (f'{str(cat)}')
                # print (f'Class output -->{repr(cat)}')

            
                # print (f'{cat.tags = }')
    #             index = 0
    #             for t in cat.tags:
    #                 index +=1
    #                 if t in tag_list:
    #                     pass
    #                 else:
    #                     if len(t) > 10:
    #                         print (f'{t = } {index = }')
    #                         pass
    #                     else:
    #                         tag_list.append(t)
    # tag_list.sort()
    # print (f'{tag_list = }')
    # print (*tag_list, sep='\n')
                

    with open('output.html', 'w') as outfile:
        outfile.writelines(output_lines)

