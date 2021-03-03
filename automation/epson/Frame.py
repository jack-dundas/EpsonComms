from collections import OrderedDict
import itertools, os
import json
class Frame():
    
    class Register(OrderedDict):
        MAX_ENTRIES = 16
        def __init__(self):       
            super(Frame.Register, self).__init__()        
            
        def __len__(self):
            return len(self.keys())
        

    class IntRegister(Register):

        name="Int Register"
        format_str = "{:05d}"
        def __init__(self, data_dict=dict()):
            super(Frame.Register, self).__init__()
            for k,v in data_dict.items():
                self[k] = v
            
        def __repr__(self):
            values = ["{:05d}".format(val) for val in self.values()]
            values_with_padding = [*values, *[self.format_str.format(0) for i in range(self.MAX_ENTRIES - len(values))]]
            return_str = ",".join(values_with_padding)
            return return_str
        
        def __setitem__(self, key, item):
            if isinstance(item, int) == False or isinstance(item, bool) == True:
                raise Exception("Int Register can only accept Int values, {item} is of type {type}".format(item=item, type=type(item)))
            if len(self) < self.MAX_ENTRIES:
                super(Frame.Register, self).__setitem__(key, item)
            else:
                raise Exception("Register Full")
            
    class BoolRegister(Register):
        name="Bool Register"
        PADDING_VALUE = 0
        def __init__(self, data_dict=dict()):
            super(Frame.Register, self).__init__()
            for k,v in data_dict.items():
                self[k] = v
            
        def __repr__(self):
            values = ["{}".format(int(val)) for val in self.values()]
            values_with_padding = [*values, *["{}".format(0) for i in range(self.MAX_ENTRIES - len(values))]]
            return_str = ",".join(values_with_padding)
            return return_str
        
        def __setitem__(self, key, item):

            if isinstance(item, bool) == False:                       
                raise Exception("Bool Register can only accept bool values, {item} is of type {type}".format(item=item, type=type(item)))

                
            if len(self) < self.MAX_ENTRIES:
                super(Frame.Register, self).__setitem__(key, item)
            else:
                raise Exception("Register Full")
    
    class FloatRegister(Register):
        name="Float Register"
        MAX_STRING_LENGTH = 255
        MAX_FLOAT_WIDTH = 10
        PADDING_VALUE = "-"
        format_str = "{:" + str(MAX_FLOAT_WIDTH) + "f}"
        
        def __init__(self, data_dict=dict()):
            super(Frame.Register, self).__init__()
            for k,v in data_dict.items():
                self[k]=v
            
        def __repr__(self):
            values = [self._float_to_string(val) for val in self.values()]
            return_str = ",".join(values)
            return_str_padding = return_str + self.PADDING_VALUE * (self.MAX_STRING_LENGTH - len(return_str))
            return return_str
        
        def __len__(self):
            return len(str(self))
        
        def __setitem__(self, key, item):
            

            if isinstance(item, float) == False:                       
                raise Exception("Float Register can only accept float values, {item} is of type {type}".format(item=item, type=type(item)))
            
            current_length = len(self)
            item_str = self._float_to_string(item)
            item_length = len(item_str)
            if current_length + item_length > self.MAX_STRING_LENGTH:
                raise Exception("Register Full")
            
            super(Frame.Register, self).__setitem__(key, item)
            
        def _float_to_string(self,float_val):
            float_str = self.format_str.format(float_val)
            float_str = float_str.lstrip()
            if float(float_str) == 0:
                float_str = "0"
            else:
                float_str = float_str.rstrip('0')

            return float_str

    
    def _get_register(self, var_name, var_val):

        if isinstance(var_val, bool):
            return self.bool_registers
        elif isinstance(var_val, int):
            return self.int_registers
        elif isinstance(var_val, float):
            return self.float_registers
        else:
            # return ("Received [{}]={}".format(var_name, var_val))
            raise Exception("Given variable [{}]={} cannot be of type {}".format(var_name,var_val, type(var_val)))
    
    def __init__(self):
        
        with open('automation/epson/epson_frame.json', "w+") as json_file:
            try:
                data = json.load(json_file)
                self.int_registers = Frame.IntRegister(data_dict = data['int_registers'])
                self.bool_registers = Frame.BoolRegister(data_dict = data['bool_registers'])
                self.float_registers = Frame.FloatRegister(data_dict = data['float_registers'])
            except json.decoder.JSONDecodeError:
                #empty file!
                self.int_registers = Frame.IntRegister()
                self.bool_registers = Frame.BoolRegister()
                self.float_registers = Frame.FloatRegister()
        self.registers = [self.int_registers, self.bool_registers, self.float_registers]
        
    def __repr__(self):
        return self.comm_str()
    
    def __len__(self):
        frame_length = 0
        for reg in [self.int_registers, self.bool_registers, self.float_registers]:
            frame_length += len(reg)
        return frame_length
    
    def __getitem__(self, key):
        for item in self._items():
            if key == item[0]:
                return item[1]
        else:
            raise KeyError("Key {} does not exist".format(key))

        

    def __setitem__(self, key, item, update=False):
        #helper lambda
        different_type = lambda a,b: not isinstance(a, type(b))

        #logic
        item_exists = key in self._keys()
        if item_exists:
            current_val = self[key]
            if different_type(item, current_val):
                #if the current val for this key is a float, we should also allow an integer (after converting) to update it
                if isinstance(current_val, float) and isinstance(item, int) and isinstance(item, bool) == False:
                    item = float(item)
                    register = self.float_registers
                    register.__setitem__(key,item)
                    return "updated var {key} to {item}!".format(key=key, item=item)
                else:
                    raise KeyError("Cannot create object {key}[{val}], key={key} already in use".format(key=key, val = item))

            register = self._get_register(key, item)
            register.__setitem__(key, item)
            return "updated var {key} to {item}!".format(key=key, item=item)
        else:
            register = self._get_register(key, item)
            register.__setitem__(key, item)
            return "created new var {key} set to {item}".format(key=key,item=item)
            


    def _items(self):
        return list(itertools.chain(self.int_registers.items(), self.bool_registers.items(), self.float_registers.items()))
    
    def _keys(self):
        return list(itertools.chain(self.int_registers.keys(), self.bool_registers.keys(), self.float_registers.keys()))

    def comm_str(self):
        strings=[]
        for register in [self.int_registers, self.bool_registers, self.float_registers]:
            strings.append(str(register))
        return_string = "\r\n".join(strings)
        return return_string
    
    def html_str(self):
        registers_html = '''
        <fieldset width:fit-content;">
            <legend>{register_name}</legend>
            <table>
            <tr>{header_row}</tr>
            <tr>{data_row}</tr>
            </table>
        </fieldset>
        
        '''
        response=[]
        for register in [self.int_registers, self.bool_registers, self.float_registers]:
            header_row = "".join(["<th  style='border: 1px solid black;'>{varname}</th>".format(varname = key) for key in register.keys()])
            data_row= "".join(["<th style='border: 1px solid black;'>{varval}</th>".format(varval = val) for val in register.values()])
            response.append(registers_html.format(register_name=register.name, header_row = header_row, data_row=data_row))
        return "".join(response)
    
    def pretty_str(self):
        ret = [
        '<div>{}</div>'.format("Current_Frame"),
        '<hr>',
        '<div>{}</div>'.format("Length:\t{}".format(len(self))),
        '<div>{}</div>'.format("Bool Items: {}/{}".format(len(self.bool_registers), self.BoolRegister.MAX_ENTRIES)),
        '<div>{}</div>'.format("Int Items: {}/{}".format(len(self.int_registers), self.IntRegister.MAX_ENTRIES)),
        '<div>{}</div>'.format("Float Length: {}/{}".format(len(self.float_registers), self.FloatRegister.MAX_STRING_LENGTH)),
        "<hr>",
        self.html_str(),
        "<hr>",
        "<div><h4>Commstr:</h4>{}</div>".format(self.comm_str())
        ]
        return_string = '<div style="margin: auto; width:80%;">{}</div>'.format("".join(ret))
        return return_string
        
    def save_to_json(self):
        save_location = os.path.join(os.path.dirname(__file__), "epson_frame.json")
        with open(save_location, 'a') as savefile:
            json.dump(self.__dict__, savefile)
        



if __name__ == "__main__":
    
   
    # test_frame1 = Frame()
    # test_frame1["test_int"]=10
    # test_frame1["test_float"]=12.5
    # test_frame1["test_bool"] = True
    # print(test_frame1)
    
    # if input("Overwrite epson_frame.json with test values? [Y/N]") =="N":
    #     raise SystemExit
    
    test_frame2 = Frame()
    for i in range(10):
        test_frame2["test_b"+str(i)] = True if i%2 == 0 else False
        test_frame2["test_i"+str(i)] = 1*i
        test_frame2["test_f"+str(i)] = 1.252*i
    
    test_frame2.pretty_str()
    
    # test_frame2.save_to_json()
    
