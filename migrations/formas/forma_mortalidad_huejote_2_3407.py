 
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
  "form_id": 5211,
  "form_pages": [
    {
      "page_fields": [
        {
          "default_value": "",
          "field_type": "date",
          "required": true,
          "groups_fields": [],
          "validations": {},
          "field_id": "561d662423d3fd6f1eb9747d",
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
          "field_id": "561d662423d3fd6f1eb9747e",
          "label": "Granja",
          "visible": true,
          "options": [
            {
              "points": null,
              "selected": false,
              "value": "huejote_2",
              "label": "Huejote 2"
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
          "field_type": "group",
          "required": true,
          "groups_fields": [
            "{'$oid': '561d662423d3fd6f1eb97480'}",
            "{'$oid': '561d662423d3fd6f1eb97481'}",
            "{'$oid': '561d662423d3fd6f1eb97482'}"
          ],
          "validations": {},
          "field_id": "561d662423d3fd6f1eb9747f",
          "label": "Mortalidad",
          "visible": true,
          "options": [],
          "grading_criteria": {},
          "properties": {
            "max": 0,
            "displayInReverse": false,
            "min": 0
          }
        },
        {
          "default_value": "",
          "field_type": "radio",
          "validations": {},
          "group": {
            "group_set_id": 0,
            "group_id": "561d662423d3fd6f1eb9747f"
          },
          "groups_fields": [],
          "required": true,
          "field_id": "561d662423d3fd6f1eb97480",
          "label": "Caseta",
          "visible": true,
          "options": [
            {
              "points": null,
              "selected": false,
              "value": "caseta_1",
              "label": "Caseta 1"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_2",
              "label": "Caseta 2"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_3",
              "label": "Caseta 3"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_4",
              "label": "Caseta 4"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_5",
              "label": "Caseta 5"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_6",
              "label": "Caseta 6"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_7",
              "label": "Caseta 7"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_8",
              "label": "Caseta 8"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_9",
              "label": "Caseta 9"
            },
            {
              "points": null,
              "selected": false,
              "value": "caseta_10",
              "label": "Caseta 10"
            }
          ],
          "grading_criteria": {},
          "properties": {
            "selected": 0,
            "openChoice": false,
            "orientation": "vertical",
            "custom": null
          }
        },
        {
          "default_value": "",
          "field_type": "radio",
          "validations": {},
          "group": {
            "group_set_id": 0,
            "group_id": "561d662423d3fd6f1eb9747f"
          },
          "groups_fields": [],
          "required": true,
          "field_id": "561d662423d3fd6f1eb97481",
          "label": "Causa de muerte",
          "visible": true,
          "options": [
            {
              "points": null,
              "selected": false,
              "value": "postura_interna",
              "label": "Postura interna"
            },
            {
              "points": null,
              "selected": false,
              "value": "prolapso",
              "label": "Prolapso"
            },
            {
              "points": null,
              "selected": false,
              "value": "respiratorio",
              "label": "Respiratorio"
            },
            {
              "points": null,
              "selected": false,
              "value": "digestivo",
              "label": "Digestivo"
            },
            {
              "points": null,
              "selected": false,
              "value": "otra",
              "label": "Otra"
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
          "validations": {},
          "group": {
            "group_set_id": 0,
            "group_id": "561d662423d3fd6f1eb9747f"
          },
          "groups_fields": [],
          "required": true,
          "field_id": "561d662423d3fd6f1eb97482",
          "label": "Total aves muertas",
          "visible": true,
          "options": [],
          "grading_criteria": {},
          "properties": {
            "numberOfDecimals": "",
            "notification": {
              "notification_criteria": {
                "less": [],
                "equal": [],
                "greater": [],
                "between": []
              },
              "send_alert": {
                "message": "",
                "email": [],
                "subject": "alta mortalidad de liebres"
              }
            },
            "step": 1,
            "size": "small",
            "custom": null
          }
        },
        {
          "default_value": "",
          "field_type": "integer",
          "required": true,
          "groups_fields": [],
          "validations": {},
          "field_id": "561d662423d3fd6f1eb97483",
          "label": "Total de aves muertas",
          "visible": true,
          "options": [],
          "grading_criteria": {},
          "properties": {
            "numberOfDecimals": "",
            "notification": {
              "notification_criteria": {
                "less": [],
                "equal": [],
                "greater": [
                  {
                    "value": 197
                  }
                ],
                "between": []
              },
              "send_alert": {
                "embed_company_picture": true,
                "sender": "OWNER_EMAIL",
                "send_pdf": true,
                "message": "El usuario {{record.user.name}} ha registrado una mortalidad de {{record.answers.5589a09c01a4de7bba84fb50}} aves en la granja  {{record.answers.5589a09c01a4de7bba84fb4e}} con fecha {{record.answers.5589a09c01a4de7bba84fb4d}}.\n\nEste aviso se genera cuando la mortalidad supera el 0.1%",
                "subject": "Mortalidad Alta en la granja {{record.answers.5589a09c01a4de7bba84fb4e}}",
                "email": [
                  "amartin@sanfandila.com",
                  "jsolis@sanfandila.com",
                  "jjvega@sanfandila.com"
                ],
                "resend": "DONT_RESEND"
              }
            },
            "step": 1,
            "size": "small",
            "custom": null
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
      "field_id": "561d662423d3fd6f1eb9747d",
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
      "field_id": "561d662423d3fd6f1eb9747e",
      "label": "Granja",
      "visible": true,
      "options": [
        {
          "points": null,
          "selected": false,
          "value": "huejote_2",
          "label": "Huejote 2"
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
      "field_type": "group",
      "required": true,
      "groups_fields": [
        {
          "$oid": "561d662423d3fd6f1eb97480"
        },
        {
          "$oid": "561d662423d3fd6f1eb97481"
        },
        {
          "$oid": "561d662423d3fd6f1eb97482"
        }
      ],
      "validations": {},
      "field_id": "561d662423d3fd6f1eb9747f",
      "label": "Mortalidad",
      "visible": true,
      "options": [],
      "grading_criteria": {},
      "properties": {
        "max": 0,
        "displayInReverse": false,
        "min": 0
      }
    },
    {
      "default_value": "",
      "field_type": "radio",
      "validations": {},
      "group": {
        "group_set_id": 0,
        "group_id": {
          "$oid": "561d662423d3fd6f1eb9747f"
        }
      },
      "groups_fields": [],
      "required": true,
      "field_id": "561d662423d3fd6f1eb97480",
      "label": "Caseta",
      "visible": true,
      "options": [
        {
          "points": null,
          "selected": false,
          "value": "caseta_1",
          "label": "Caseta 1"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_2",
          "label": "Caseta 2"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_3",
          "label": "Caseta 3"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_4",
          "label": "Caseta 4"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_5",
          "label": "Caseta 5"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_6",
          "label": "Caseta 6"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_7",
          "label": "Caseta 7"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_8",
          "label": "Caseta 8"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_9",
          "label": "Caseta 9"
        },
        {
          "points": null,
          "selected": false,
          "value": "caseta_10",
          "label": "Caseta 10"
        }
      ],
      "grading_criteria": {},
      "properties": {
        "selected": 0,
        "openChoice": false,
        "orientation": "vertical",
        "custom": null
      }
    },
    {
      "default_value": "",
      "field_type": "radio",
      "validations": {},
      "group": {
        "group_set_id": 0,
        "group_id": {
          "$oid": "561d662423d3fd6f1eb9747f"
        }
      },
      "groups_fields": [],
      "required": true,
      "field_id": "561d662423d3fd6f1eb97481",
      "label": "Causa de muerte",
      "visible": true,
      "options": [
        {
          "points": null,
          "selected": false,
          "value": "postura_interna",
          "label": "Postura interna"
        },
        {
          "points": null,
          "selected": false,
          "value": "prolapso",
          "label": "Prolapso"
        },
        {
          "points": null,
          "selected": false,
          "value": "respiratorio",
          "label": "Respiratorio"
        },
        {
          "points": null,
          "selected": false,
          "value": "digestivo",
          "label": "Digestivo"
        },
        {
          "points": null,
          "selected": false,
          "value": "otra",
          "label": "Otra"
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
      "validations": {},
      "group": {
        "group_set_id": 0,
        "group_id": {
          "$oid": "561d662423d3fd6f1eb9747f"
        }
      },
      "groups_fields": [],
      "required": true,
      "field_id": "561d662423d3fd6f1eb97482",
      "label": "Total aves muertas",
      "visible": true,
      "options": [],
      "grading_criteria": {},
      "properties": {
        "numberOfDecimals": "",
        "notification": {
          "notification_criteria": {
            "less": [],
            "equal": [],
            "greater": [],
            "between": []
          },
          "send_alert": {
            "message": "",
            "email": [],
            "subject": "alta mortalidad de liebres"
          }
        },
        "step": 1,
        "size": "small",
        "custom": null
      }
    },
    {
      "default_value": "",
      "field_type": "integer",
      "required": true,
      "groups_fields": [],
      "validations": {},
      "field_id": "561d662423d3fd6f1eb97483",
      "label": "Total de aves muertas",
      "visible": true,
      "options": [],
      "grading_criteria": {},
      "properties": {
        "numberOfDecimals": "",
        "notification": {
          "notification_criteria": {
            "less": [],
            "equal": [],
            "greater": [
              {
                "value": 197
              }
            ],
            "between": []
          },
          "send_alert": {
            "embed_company_picture": true,
            "sender": "OWNER_EMAIL",
            "send_pdf": true,
            "message": "El usuario {{record.user.name}} ha registrado una mortalidad de {{record.answers.5589a09c01a4de7bba84fb50}} aves en la granja  {{record.answers.5589a09c01a4de7bba84fb4e}} con fecha {{record.answers.5589a09c01a4de7bba84fb4d}}.\n\nEste aviso se genera cuando la mortalidad supera el 0.1%",
            "subject": "Mortalidad Alta en la granja {{record.answers.5589a09c01a4de7bba84fb4e}}",
            "email": [
              "amartin@sanfandila.com",
              "jsolis@sanfandila.com",
              "jjvega@sanfandila.com"
            ],
            "resend": "DONT_RESEND"
          }
        },
        "step": 1,
        "size": "small",
        "custom": null
      }
    }
  ],
  "created_at": 1444767268224,
  "private_url": "template-view/5211",
  "updated_at": 1444767276314,
  "emails": [],
  "allow_page_navigation": true,
  "advanced_options": {
    "active": false
  },
  "templates": [],
  "notification": {
    "active": true
  },
  "force_owner_logo": false,
  "resource_uri": "/api/infosync/form/5211/",
  "name": "Huevo - Mortalidad Huejote 2(copy)",
  "public": false,
  "description": ""
}