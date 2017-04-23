 
{
  "email_configuration": {
    "reply_to": "USER_EMAIL",
    "emails": [],
    "embed_fields": []
  },
  "edit_registers": true,
  "confirmation": {
    "message": "\u00a1Su informaci\u00f3n fue capturada!",
    "redirect_url": "default",
    "button_message": "Mandar respuestas"
  },
  "form_id": 3525,
  "form_pages": [
    {
      "page_fields": [
        {
          "default_value": "",
          "field_type": "date",
          "required": true,
          "groups_fields": [],
          "validations": {},
          "field_id": "561d681123d3fd6f1eb97496",
          "label": "Fecha de produccion",
          "visible": true,
          "options": [],
          "grading_criteria": {},
          "properties": {
            "format": "vertical",
            "custom": null
          }
        },
        {
          "default_value": "",
          "field_type": "radio",
          "required": true,
          "groups_fields": [],
          "validations": {},
          "field_id": "561d681123d3fd6f1eb97497",
          "label": "Granja",
          "visible": true,
          "options": [
            {
              "points": null,
              "selected": false,
              "value": "liebres",
              "label": "Liebres"
            }
          ],
          "grading_criteria": {},
          "properties": {
            "notification": {
              "notification_criteria": {
                "equal": []
              },
              "send_alert": {
                "message": "",
                "email": [],
                "subject": ""
              }
            },
            "selected": 0,
            "openChoice": false,
            "orientation": "vertical",
            "custom": null
          }
        }
      ],
      "page_name": "Fecha"
    },
    {
      "page_fields": [
        {
          "default_value": "",
          "field_type": "integer",
          "required": true,
          "groups_fields": [],
          "validations": {},
          "field_id": "561d681123d3fd6f1eb97498",
          "label": "Total de aves muertas",
          "visible": true,
          "options": [],
          "grading_criteria": {},
          "properties": {
            "min": -11,
            "max": 8,
            "custom": null,
            "numberOfDecimals": "",
            "step": 1,
            "notification": {
              "notification_criteria": {
                "less": [],
                "equal": [],
                "greater": [
                  {
                    "value": 111
                  }
                ],
                "between": []
              },
              "send_alert": {
                "message": "Se super\u00f3 el limite de mortalidad establecido (60 aves).",
                "sender": "OWNER_EMAIL",
                "subject": "Alta mortalidad Liebres",
                "email": [
                  "jjvega@sanfandila.com",
                  "jsolis@sanfandila.com",
                  "amartin@sanfandila.com"
                ],
                "resend": "DONT_RESEND"
              }
            },
            "size": "small"
          }
        }
      ],
      "page_name": "Mortalidad"
    }
  ],
  "grading": {
    "active": false,
    "grade_type": "points"
  },
  "enable_geolocation": true,
  "fields": [
    {
      "default_value": "",
      "field_type": "date",
      "required": true,
      "groups_fields": [],
      "validations": {},
      "field_id": "561d681123d3fd6f1eb97496",
      "label": "Fecha de produccion",
      "visible": true,
      "options": [],
      "grading_criteria": {},
      "properties": {
        "format": "vertical",
        "custom": null
      }
    },
    {
      "default_value": "",
      "field_type": "radio",
      "required": true,
      "groups_fields": [],
      "validations": {},
      "field_id": "561d681123d3fd6f1eb97497",
      "label": "Granja",
      "visible": true,
      "options": [
        {
          "points": null,
          "selected": false,
          "value": "liebres",
          "label": "Liebres"
        }
      ],
      "grading_criteria": {},
      "properties": {
        "notification": {
          "notification_criteria": {
            "equal": []
          },
          "send_alert": {
            "message": "",
            "email": [],
            "subject": ""
          }
        },
        "selected": 0,
        "openChoice": false,
        "orientation": "vertical",
        "custom": null
      }
    },
    {
      "default_value": "",
      "field_type": "integer",
      "required": true,
      "groups_fields": [],
      "validations": {},
      "field_id": "561d681123d3fd6f1eb97498",
      "label": "Total de aves muertas",
      "visible": true,
      "options": [],
      "grading_criteria": {},
      "properties": {
        "min": -11,
        "max": 8,
        "custom": null,
        "numberOfDecimals": "",
        "step": 1,
        "notification": {
          "notification_criteria": {
            "less": [],
            "equal": [],
            "greater": [
              {
                "value": 111
              }
            ],
            "between": []
          },
          "send_alert": {
            "message": "Se super\u00f3 el limite de mortalidad establecido (60 aves).",
            "sender": "OWNER_EMAIL",
            "subject": "Alta mortalidad Liebres",
            "email": [
              "jjvega@sanfandila.com",
              "jsolis@sanfandila.com",
              "amartin@sanfandila.com"
            ],
            "resend": "DONT_RESEND"
          }
        },
        "size": "small"
      }
    }
  ],
  "created_at": 1444767761975,
  "private_url": "template-view/3525",
  "updated_at": 1444767769863,
  "emails": [],
  "allow_page_navigation": true,
  "advanced_options": {
    "active": false
  },
  "templates": [],
  "notification": {
    "active": false
  },
  "force_owner_logo": false,
  "resource_uri": "/api/infosync/form/3525/",
  "name": "Huevo - Mortalidad Liebres(copy)",
  "public": false,
  "description": ""
}