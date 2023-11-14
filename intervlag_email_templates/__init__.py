from . import models
from odoo import api, SUPERUSER_ID

def _intervlag_email_templates(cr):
    """This function used to manipulate the default email templates to
    intervlag email templates"""
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Intervalg Reset password
    reset_password = env.ref("auth_signup.reset_password_email")
    reset_password_body_template = f"""<p style="margin-bottom: 0px;">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@900&amp;amp;display=swap');
  </style>
</p>
<div style="font-size:13px;font-family:&quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;padding:0px;width:600px;margin:auto;background: #FFFFFF repeat top /100%;color:#777777">
  <table style="border-collapse:collapse;max-width:600px;margin:0 auto;" width="100%" cellspacing="0" cellpadding="0" border="0" align="center">
    <tbody>
      <tr>
        <td style="font-size:12px" width="200" valign="center">
          <t t-if="object.partner_id.lang != 'nl_NL'" data-oe-t-group="0" data-oe-t-selectable="true" data-oe-t-group-active="true" data-oe-t-inline="true">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/3a194bcf-d3b1-45af-a9d5-91a06f109982.png" class="mcnRetinaImage" style="border-style:none;vertical-align:middle;border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; display: inline !important; width: auto;" width="0" height="0" align="middle">
          </t>
          <t t-else="" data-oe-t-selectable="true" data-oe-t-group="0" data-oe-t-inline="true">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/72205120-7b22-4410-97fb-43e4149c0183.png" class="mcnRetinaImage" style="border-style:none;vertical-align:middle;border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; display: inline !important; width: auto;" width="0" height="0" align="middle">
          </t>
        </td>
      </tr>
      <tr>
        <td style="min-width:600px;background-color: rgb(0, 154, 147);background-image: none;background-repeat: repeat;background-position: center center;background-size: cover;border-top: 0px;border-bottom: 0px;padding-top: 40px;padding-bottom: 50px;" align="center">
          <a href="#" style="background-color:transparent;text-decoration-thickness:auto;color:rgb(0, 135, 132);display:block;padding: 9px;">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/3d993262-92ab-4463-b158-67b07d07a70d.gif" class="mcnRetinaImage" style="border-style:none;border-width:0px;height: auto;outline: none;vertical-align: bottom;max-width: 360px;padding-bottom: 0px;display: inline !important;width: auto;" width="0" height="0" align="middle">
          </a>
          <div style="font-size:13px;font-family:Helvetica;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;padding-top:36px;">
            <h3 style="line-height:1.2;font-family:'Raleway', sans-serif;font-weight: 900;font-size: 24px;color: #fff;text-transform: uppercase;margin-bottom: 14px;">PASSWORD RESET.</h3>
            <span style="color:#fff;">Dear <t t-out="object.name" contenteditable="false" data-oe-t-inline="true"></t>, </span>
            <br>
            <p style="margin:0px;font-size:13px;font-family:&quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;color:#fff;padding: 22px 0px;">A password reset has been requested for your username via our website. <br>You can change your password using the button below, <br>it remains valid for the next 24 hours. </p>
          </div>
          <a title="CHANGE PASSWORD" target="_blank" style="text-decoration-thickness:auto;text-size-adjust:100%;display: inline-block;font-weight: bold;line-height: 12px;text-align: center;color: rgb(255, 255, 255);border-radius: 50px;background-color: rgb(227, 6, 19);font-family: Arial;font-size: 12px;padding: 10px;line-height: 12px;text-decoration: none;margin-bottom: 18px;" t-attf-href="{{ object.signup_url }}">CHANGE PASSWORD</a>
        </td>
      </tr>
      <tr>
        <td style="padding-top:50px;padding-bottom: 45px;" align="center">
          <div style="text-size-adjust:100%;word-break: break-word;color: rgb(102, 102, 102);font-family: Helvetica;font-size: 13px;line-height: 19.5px;text-align:center;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;">
            <p style="margin:0px;font-size:13px;font-family:&quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">Did you not request the reset yourself? Then you can ignore this email.</p>
            <p style="margin:0px;font-size:13px;font-family:&quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">Best regards,</p>
            <t t-if="user.signature" data-oe-t-group="1" data-oe-t-group-active="true">
              <p style="margin:0px;font-size:13px;font-family:&quot;Lucida Grande&quot;, Helvetica, Verdana, Arial, sans-serif;">
                <t t-out="user.signature" contenteditable="false" data-oe-t-inline="true"></t>
              </p>
            </t>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <table style="border-collapse:collapse;" width="100%" cellspacing="0" cellpadding="0">
    <tbody>
      <tr style="background-color:#000000;padding-top:25px;padding-bottom:25px;color:#ffffff;font-family:Helvetica;font-size:12px;line-height:150%;text-align:center;font-weight:normal;">
        <td class="mcnTextContent" style="text-align:left;padding-left:20px;padding-top:25px;padding-bottom:25px;" valign="top">
          <t t-if="object.partner_id.lang != 'nl_NL'" data-oe-t-group="2" data-oe-t-selectable="true" data-oe-t-group-active="true" data-oe-t-inline="true">
            <img data-file-id="2126449" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/9830b47b-2880-4efc-af54-7f725f3f6fe5.png" style="border-style:none;vertical-align:middle;border:0px initial;width: 108px; height: 63px; margin: 0px;" width="108" height="63">
            <br>
            <br>
            <img data-file-id="2154085" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/878e68ac-df48-431d-95cc-e8f1b8222a46.png" style="border-style:none;vertical-align:middle;border:0px;width: 264px; height: 34px; margin: 0px;" width="264" height="34">
          </t>
          <t t-else="" data-oe-t-selectable="true" data-oe-t-group="2" data-oe-t-inline="true">
            <img data-file-id="2126449" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/b695d881-ce04-49c8-8520-90453dbb5402.png" style="border-style:none;vertical-align:middle;border:0px initial;width: 108px; height: 63px; margin: 0px;" width="108" height="63">
            <br>
            <br>
            <img data-file-id="2154085" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/f20f334e-8abf-467d-adbd-48cadc26c7c0.png" style="border-style:none;vertical-align:middle;border:0px;width: 264px; height: 34px; margin: 0px;" width="264" height="34">
          </t>
        </td>
        <td class="mcnTextContent" style="width:40%;font-size:12px; padding-top:25px;padding-bottom:25px;color:white;text-align: left;" valign="top"> Intervlag <br> Tempelhof 1 <br> 3045 PV Rotterdam <br> Nederland <br>
          <br>
          <a href="callto:+31%20(0)10%20785%2067%2066" target="_blank" style="background-color:transparent;text-decoration-thickness:auto;text-decoration:none;color:white;">+31 (0)10 785 67 66</a>
          <br>
          <a style="background-color:transparent;text-decoration-thickness:auto;text-decoration:underline;color:white;" href="mailto:info@intervlag.nl" target="_blank">info@intervlag.nl</a>
          <br>
          <a style="background-color:transparent;text-decoration-thickness:auto;text-decoration:underline;color:white;" href="http://www.intervlag.nl" target="_blank">www.intervlag.nl</a>
        </td>
      </tr>
    </tbody>
  </table>
</div>"""
    reset_password.write({
        "body_html": reset_password_body_template
    })

    #Intervlag Delivery: Send by Email1
    delivery_send_by_email1 = env.ref("stock.mail_template_data_delivery_confirmation")
    print("delivery_send_by_email1",delivery_send_by_email1)
    delivery_send_by_email1_body_template = f"""<p style="box-sizing:border-box;margin-bottom: 0px;">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@900&amp;display=swap');
  </style>
</p>
<div style="padding:0px;width:600px;margin:auto;background: #FFFFFF repeat top /100%;color:#777777">
  <table cellspacing="0" cellpadding="0" align="center" border="0" width="100%" style="box-sizing:border-box;border-collapse:collapse; max-width:600px;margin:0 auto;">
    <tbody>
      <tr>
        <td valign="center" width="200" style="font-size:12px">
          <t t-if="object.partner_id.lang != 'nl_NL'" data-oe-t-group="0" data-oe-t-selectable="true" data-oe-t-group-active="true" data-oe-t-inline="true">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/3a194bcf-d3b1-45af-a9d5-91a06f109982.png" class="mcnRetinaImage" style="border-style:none;box-sizing:border-box;outline-width:initial;outline-style:none;outline-color:initial;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;border-width: 0px; height: 116px; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; width: 600px; display: inline ;" align="middle" width="600px" height="116">
          </t>
          <t t-else="" data-oe-t-selectable="true" data-oe-t-group="0" data-oe-t-inline="true">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/72205120-7b22-4410-97fb-43e4149c0183.png" class="mcnRetinaImage" style="border-style:none;box-sizing:border-box;outline-width:initial;outline-style:none;outline-color:initial;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;border-width: 0px; height: 116px; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; width: 600px; display: inline ;" align="middle" width="600px" height="116">
          </t>
        </td>
      </tr>
      <tr>
        <td align="center" style="background-color:#f9b000;padding-top: 40px;padding-bottom: 50px;">
          <div>
            <h3 style="box-sizing:border-box;line-height:1.2;font-family:'Raleway', sans-serif;font-weight: 900;font-size: 24px;color: #fff;margin: 0px 0px 48px 0px;text-transform: uppercase;">YOUR ORDER IS COMPLETE! </h3>
            <div style="color:#ffffff;font-family: Helvetica;font-size: 13px;line-height: 19.5px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;">
              <p style="margin:0px 0 12px 0;box-sizing:border-box;">Yes! Your order <t t-out="object.origin" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t> is complete. </p>
              <t t-if="object.sale_id.client_order_ref" data-oe-t-group="1" data-oe-t-group-active="true" data-oe-t-inline="true"> Your order reference: <t t-out="object.sale_id.client_order_ref" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
              </t>
              <br>
              <t t-if="object.carrier_tracking_ref" data-oe-t-group="2" data-oe-t-group-active="true">
                <t t-if="object.carrier_tracking_url" data-oe-t-group="3" data-oe-t-selectable="true" data-oe-t-group-active="true">
                  <p style="margin:0px 0 12px 0;box-sizing:border-box;">Did you choose the delivery option? Than this will be your tracking link:</p>
                  <a style="text-decoration:none;box-sizing:border-box;background-color:transparent;color:#008f8c;display:block;padding-top: 18px;" t-attf-href="{{object.carrier_tracking_url}}" target="_blank">
                    <img align="center" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/0a728f38-550d-41bf-946b-c44bdaaf5cb4.png" class="mcnRetinaImage" style="border-style:none;box-sizing:border-box;outline-width:initial;outline-style:none;outline-color:initial;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;border-width: 0px; height: 30px; outline: none; vertical-align: bottom; max-width: 142px; padding-bottom: 0px; width: 142px; display: inline ;" width="142px" height="30">
                  </a>
                </t>
                <t t-else="" data-oe-t-selectable="true" data-oe-t-group="3" data-oe-t-inline="true">
                  <t t-out="object.carrier_tracking_ref" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                </t>
              </t>
              <a href="#" style="text-decoration:none;box-sizing:border-box;background-color:transparent;color:#008f8c;display:block;padding-top: 45px;">
                <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/d6c9ca38-3b65-4877-a223-41db5dd5d700.gif" class="mcnRetinaImage" style="border-style:none;box-sizing:border-box;outline-width:initial;outline-style:none;outline-color:initial;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;border-width: 0px; height: 264px; outline: none; vertical-align: bottom; max-width: 264px; padding-bottom: 0px; width: 264px; display: inline ;" align="center" width="264px" height="264">
              </a>
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td align="center" style="background-color:#009a93;padding-top: 50px;padding-bottom: 45px;">
          <a href="#" style="text-decoration:none;box-sizing:border-box;background-color:transparent;color:#008f8c;display:block;padding: 9px;">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/f02de05d-7a3b-45bc-8420-6bf939347698.png" class="mcnRetinaImage" style="border-style:none;box-sizing:border-box;outline-width:initial;outline-style:none;outline-color:initial;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;border-width: 0px; height: 78px; outline: none; vertical-align: bottom; max-width: 72px; padding-bottom: 0px; width: 72px; display: inline ;" align="middle" width="72px" height="78">
          </a>
          <h3 style="box-sizing:border-box;line-height:1.2;font-family:'Raleway', sans-serif;font-weight: 900;padding-top: 9px;font-size:24px;color:#fff;text-transform: uppercase;margin: 0px;padding-bottom: 38px;">DID YOU CHOOSE THE PICK UP OPTION? </h3>
          <t t-if="object.company_id" data-oe-t-group="4" data-oe-t-group-active="true">
            <div>
              <p style="margin:0px 0 12px 0;box-sizing:border-box;color:#fff;font-family: Helvetica;padding-bottom: 28px;">Your order is now ready for pick up. This is our address:</p>
              <div style="color:#fff;font-family: Helvetica;font-size: 13px;background-color: #007973;padding-top: 29px;padding-bottom: 29px;line-height: 19.5px;">
                <span style="display:block;">
                  <t t-out="object.company_id.name" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                </span>
                <span style="display:block;">
                  <t t-out="object.company_id.street_name" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                  <t t-out="object.company_id.street_number" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                </span>
                <span style="display:block;">
                  <t t-out="object.company_id.zip" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                  <t t-out="object.company_id.city" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                </span>
                <span style="display:block;">
                  <t t-out="object.company_id.country_id.name" contenteditable="false" data-oe-t-inline="true" oe-keep-contenteditable=""></t>
                </span>
              </div>
            </div>
          </t>
        </td>
      </tr>
    </tbody>
  </table>
  <table cellspacing="0" cellpadding="0" width="100%" style="box-sizing:border-box;border-collapse:collapse;">
    <tbody>
      <tr style="background-color:#000000;padding-top:25px;padding-bottom:25px;color:#ffffff;font-family:Helvetica;font-size:12px;line-height:150%;text-align:center;font-weight:normal;">
        <td class="mcnTextContent" style="text-align:left;padding-left:20px;padding-top:25px;padding-bottom:25px;" valign="top">
          <t t-if="object.partner_id.lang != 'nl_NL'" data-oe-t-group="5" data-oe-t-selectable="true" data-oe-t-group-active="true" data-oe-t-inline="true">
            <img data-file-id="2126449" height="63" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/9830b47b-2880-4efc-af54-7f725f3f6fe5.png" style="border-style:none;box-sizing:border-box;vertical-align:middle;border: 0px initial ; width: 108px; height: 63px; margin: 0px;" width="108px">
            <br>
            <br>
            <img data-file-id="2154085" height="34" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/878e68ac-df48-431d-95cc-e8f1b8222a46.png" style="box-sizing:border-box;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;vertical-align:middle;border: 0px; width: 264px; height: 34px; margin: 0px;" width="264px">
          </t>
          <t t-else="" data-oe-t-selectable="true" data-oe-t-group="5" data-oe-t-inline="true">
            <img data-file-id="2126449" height="63" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/b695d881-ce04-49c8-8520-90453dbb5402.png" style="border-style:none;box-sizing:border-box;vertical-align:middle;border: 0px initial ; width: 108px; height: 63px; margin: 0px;" width="108px">
            <br>
            <br>
            <img data-file-id="2154085" height="34" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/f20f334e-8abf-467d-adbd-48cadc26c7c0.png" style="box-sizing:border-box;border-left-width:0px;border-bottom-width:0px;border-right-width:0px;border-top-width:0px;vertical-align:middle;border: 0px; width: 264px; height: 34px; margin: 0px;" width="264px">
          </t>
        </td>
        <td class="mcnTextContent" style="width:40%;font-size:12px; padding-top:25px;padding-bottom:25px;color:white;text-align: left;" valign="top"> Intervlag <br> Tempelhof 1 <br> 3045 PV Rotterdam <br> Nederland <br>
          <br>
          <a href="callto:+31 (0)10 785 67 66" target="_blank" style="box-sizing:border-box;background-color:transparent;text-decoration:none;color:white;">+31 (0)10 785 67 66</a>
          <br>
          <a style="box-sizing:border-box;background-color:transparent;text-decoration:underline;color:white;" href="mailto:info@intervlag.nl" target="_blank">info@intervlag.nl</a>
          <br>
          <a style="box-sizing:border-box;background-color:transparent;text-decoration:underline;color:white;" href="http://www.intervlag.nl" target="_blank">www.intervlag.nl</a>
        </td>
      </tr>
    </tbody>
  </table>
</div>"""
    delivery_send_by_email1.write({
        "body_html": delivery_send_by_email1_body_template,
        "name": 'Delivery: Send by Email1',
        "subject": "Your order is complete"
    })

    # Intervlag Invoicing: Invoice email1
    invoicing_invoice_email1 = env.ref("account.email_template_edi_invoice")
    print("invoicing_invoice_email1",invoicing_invoice_email1)
    invoicing_invoice_body_template_email1 = f"""<style>
  @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@900&amp;display=swap');
</style>
<div style="padding:0px;width:600px;margin:auto;background: #FFFFFF repeat top /100%;color:#777777">
  <table cellspacing="0" cellpadding="0" align="center" border="0" width="100%" style=" max-width:600px;margin:0 auto;">
    <tbody>
      <tr>
        <td valign="center" width="200" style="font-size:12px">
          <t t-if="object.partner_id.lang != 'nl_NL'">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/3a194bcf-d3b1-45af-a9d5-91a06f109982.png" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; display: inline !important; width: auto;" align="middle" />
          </t>
          <t t-else="">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/72205120-7b22-4410-97fb-43e4149c0183.png" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; display: inline !important; width: auto;" align="middle" />
          </t>
        </td>
      </tr>
      <tr>
        <td align="center" style="background-color:rgb(10, 123, 117);padding-top: 50px;padding-bottom: 50px;">
          <div>
            <h3 style="font-family:'Raleway', sans-serif;font-weight: 900;font-size: 24px;color: #fff;margin: 0px;text-transform:uppercase">HERE’S YOUR INVOICE</h3>
            <div style="color:rgb(255, 255, 255);font-family: Helvetica;font-size: 13px;line-height: 19.5px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;padding-top: 40px;">
              <p>Your invoice is ready for payment.</p>
              <p>Please see attached invoice number
                <t t-out="object.name" /> from
                <t t-out="object.invoice_origin" />.
              </p>
              <a href="#" style="display:block;padding-top: 45px;">
                <img align="center" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/11dd36a3-f9cc-4a65-b632-aff5e1c1753c.gif" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 264px; padding-bottom: 0px; display: inline !important; width: auto;" />
              </a>
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td align="center" style="background-color:rgb(0, 154, 147);padding-top: 50px;padding-bottom: 45px;">
          <h3 style="font-family:'Raleway', sans-serif;font-weight: 900;font-size:24px;color:#fff;text-transform:uppercase">ANY QUESTIONS?</h3>
          <div style="padding-top:40px;color: #fff;font-size: 13px;font-family: Helvetica;">
            <p>If you have any questions, don't hesitate to contact us.</p>
            <br />
            <p>Thanks for choosing Intervlag!</p>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <table cellspacing="0" cellpadding="0" width="100%">
    <tbody>
      <tr style="background-color:#000000;padding-top:25px;padding-bottom:25px;color:#ffffff;font-family:Helvetica;font-size:12px;line-height:150%;text-align:center;font-weight:normal;">
        <td class="mcnTextContent" style="text-align:left;padding-left:20px;padding-top:25px;padding-bottom:25px;" valign="top">
          <t t-if="object.partner_id.lang != 'nl_NL'">
            <img data-file-id="2126449" height="63" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/9830b47b-2880-4efc-af54-7f725f3f6fe5.png" style="border: 0px initial ; width: 108px; height: 63px; margin: 0px;" width="108" />
            <br />
            <br />
            <img data-file-id="2154085" height="34" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/878e68ac-df48-431d-95cc-e8f1b8222a46.png" style="border: 0px; width: 264px; height: 34px; margin: 0px;" width="264" />
          </t>
          <t t-else="">
            <img data-file-id="2126449" height="63" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/b695d881-ce04-49c8-8520-90453dbb5402.png" style="border: 0px initial ; width: 108px; height: 63px; margin: 0px;" width="108" />
            <br />
            <br />
            <img data-file-id="2154085" height="34" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/f20f334e-8abf-467d-adbd-48cadc26c7c0.png" style="border: 0px; width: 264px; height: 34px; margin: 0px;" width="264" />
          </t>
        </td>
        <td class="mcnTextContent" style="width:40%;font-size:12px; padding-top:25px;padding-bottom:25px;color:white;text-align: left;" valign="top"> Intervlag <br /> Tempelhof 1 <br /> 3045 PV Rotterdam <br /> Nederland <br />
          <br />
          <a href="callto:+31 (0)10 785 67 66" target="_blank" style="text-decoration:none;color:white;">+31 (0)10 785 67 66</a>
          <br />
          <a style="text-decoration:underline;color:white;" href="mailto:info@intervlag.nl" target="_blank">info@intervlag.nl</a>
          <br />
          <a style="text-decoration:underline;color:white;" href="http://www.intervlag.nl" target="_blank">www.intervlag.nl</a>
        </td>
      </tr>
    </tbody>
  </table>
</div>"""
    invoicing_invoice_email1.write({
        "body_html": invoicing_invoice_body_template_email1,
        "name": 'Invoicing: Invoice email1',
        "subject": "Here's your invoice"
    })

    #New User Registration: Send by Email
    user_registration_send_by_email = env.ref("auth_signup.mail_template_user_signup_account_created")
    user_registration_send_by_email_body_template = f"""<style>
  @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@900&amp;display=swap');
</style>
<div style="padding:0px;width:600px;margin:auto;background: #FFFFFF repeat top /100%;color:#777777">
  <table cellspacing="0" cellpadding="0" align="center" border="0" width="100%" style=" max-width:600px;margin:0 auto;">
    <tbody>
      <tr>
        <td valign="center" width="200" style="font-size:12px">
          <t t-if="object.partner_id.lang != 'nl_NL'">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/3a194bcf-d3b1-45af-a9d5-91a06f109982.png" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; display: inline !important; width: auto;" align="middle" />
          </t>
          <t t-else="">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/72205120-7b22-4410-97fb-43e4149c0183.png" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 600px; padding-bottom: 0px; display: inline !important; width: auto;" align="middle" />
          </t>
        </td>
      </tr>
      <tr>
        <td align="center" style="background-color:rgb(0, 154, 147);padding-top: 40px;padding-bottom: 50px;">
          <a href="#" style="display:block;padding: 9px;">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/78bf34c4-508a-4332-a7c3-ce20dabff4f0.png" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 100px; padding-bottom: 0px; display: inline !important; width: auto;" align="middle" />
          </a>
          <div style="padding-top:20px;">
            <h3 style="font-family:'Raleway', sans-serif;font-weight: 900;font-size: 24px;color: #fff;margin: 21px 0px;text-transform:uppercase">THANK YOU FOR SIGNING UP </h3>
            <div style="color:rgb(255, 255, 255);font-family: Helvetica;font-size: 13px;line-height: 19.5px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;padding-top: 20px;">
              <p>Intervlag works exclusively with resellers.For this reason we check your details before you can view the prices.</p>
              <br />
              <p>Within 24 hours someone will look at it. </p>
            </div>
          </div>
        </td>
      </tr>
      <tr>
        <td align="center" style="background-color:rgb(249, 176, 0);padding-top: 50px;padding-bottom: 45px;">
          <a href="#" style="display:block;padding: 9px;">
            <img src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/c2d8aba9-ecc9-4f14-9bd6-0fcf2a70fa18.png" class="mcnRetinaImage" style="border-width:0px;height: auto; outline: none; vertical-align: bottom; max-width: 54px; padding-bottom: 0px; display: inline !important; width: auto;" align="middle" />
          </a>
          <h3 style="font-family:'Raleway', sans-serif;font-weight: 900;padding-top: 9px;font-size:24px;color:#fff;text-transform:uppercase">WOULD YOU LIKE TO SEE THE PRICES FASTER?</h3>
          <div style="padding-top:32px;">
            <p style="color: #fff;font-family: Helvetica;">Call us on +49 231 29 299 202 and we'll look into it right away.</p>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  <table cellspacing="0" cellpadding="0" width="100%">
    <tbody>
      <tr style="background-color:#000000;padding-top:25px;padding-bottom:25px;color:#ffffff;font-family:Helvetica;font-size:12px;line-height:150%;text-align:center;font-weight:normal;">
        <td class="mcnTextContent" style="text-align:left;padding-left:20px;padding-top:25px;padding-bottom:25px;" valign="top">
          <t t-if="object.partner_id.lang != 'nl_NL'">
            <img data-file-id="2126449" height="63" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/9830b47b-2880-4efc-af54-7f725f3f6fe5.png" style="border: 0px initial ; width: 108px; height: 63px; margin: 0px;" width="108" />
            <br />
            <br />
            <img data-file-id="2154085" height="34" src="https://mcusercontent.com/586e1f749e29757e8c406d0c4/images/878e68ac-df48-431d-95cc-e8f1b8222a46.png" style="border: 0px; width: 264px; height: 34px; margin: 0px;" width="264" />
          </t>
          <t t-else="">
            <img data-file-id="2126449" height="63" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/b695d881-ce04-49c8-8520-90453dbb5402.png" style="border: 0px initial ; width: 108px; height: 63px; margin: 0px;" width="108" />
            <br />
            <br />
            <img data-file-id="2154085" height="34" src="https://gallery.mailchimp.com/586e1f749e29757e8c406d0c4/images/f20f334e-8abf-467d-adbd-48cadc26c7c0.png" style="border: 0px; width: 264px; height: 34px; margin: 0px;" width="264" />
          </t>
        </td>
        <td class="mcnTextContent" style="width:40%;font-size:12px; padding-top:25px;padding-bottom:25px;color:white;text-align: left;" valign="top"> Intervlag <br /> Tempelhof 1 <br /> 3045 PV Rotterdam <br /> Nederland <br />
          <br />
          <a href="callto:+31 (0)10 785 67 66" target="_blank" style="text-decoration:none;color:white;">+31 (0)10 785 67 66</a>
          <br />
          <a style="text-decoration:underline;color:white;" href="mailto:info@intervlag.nl" target="_blank">info@intervlag.nl</a>
          <br />
          <a style="text-decoration:underline;color:white;" href="http://www.intervlag.nl" target="_blank">www.intervlag.nl</a>
        </td>
      </tr>
    </tbody>
  </table>
</div>"""
    user_registration_send_by_email.write({"body_html":user_registration_send_by_email_body_template,
                                           "subject":"Thank you for Signing Up",
                                           "name" : 'New User Registration: Send by Email'
                                           })










