from twilio.rest import Client


class sendsms():

    def send(self,name , cmpny ,mno,to):

        # the following line needs your Twilio Account SID and Auth Token
        
        client = Client("AC97c237318a9b897aa14ba77982dabc3d", "714f4c5df9bb494012b4a3e1b9e0b720")
        print(name)
        print(cmpny)
        print(mno)
        print(to)
        
        msg = name + " from " + cmpny + " is here to deliver your package. Contact Number : " +mno 
        print(msg)


        # change the "from_" number to your Twilio number and the "to" number
        # to the phone number you signed up for Twilio with, or upgrade your
        # account to send SMS to any phone number
        client.messages.create(to="+919167198250", 
                            from_="+16196333974", 
                            body=msg)