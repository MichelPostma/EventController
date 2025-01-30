def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == 'hello':
        return 'Hello, I am working. If you need help, type help'
    
    elif lowered == 'help':
        return 'If you want to know what I do, please see my [Manual](https://docs.google.com/document/d/1djUGfNgCM2t-ABRU0Gs2DhUuzp5f1Rh_h9FlJczPP74/edit?pli=1&tab=t.0#heading=h.nybdllia39kl). If you need more help, type !help'
    
    elif lowered == '!help':
        return 'I am tagging my creator <@179307313977360384>. If he does not show up, please contact him yourself.'
