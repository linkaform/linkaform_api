 
{
  "email_configuration": {
    "reply_to": "USER_EMAIL",
    "emails": [],
    "embed_fields": []
  },
  "edit_registers": true,
  "confirmation": {
    "message": "\u00a1Su informaci\u00f3n fue capturada!",
    "button_message": "Mandar respuestas",
    "redirect_url": "default"
  },
  "form_id": 3398,
  "form_pages": [
    {
      "page_fields": [
        {
          "default_value": "",
          "field_type": "date",
          "required": true,
          "groups_fields": [],
          "validations": {},
          "field_id": "561d698b23d3fd6f1eb974b4",
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
          "field_id": "561d698b23d3fd6f1eb974b5",
          "label": "Granja",
          "visible": true,
          "options": [
            {
              "points": null,
              "selected": false,
              "value": "san_diego_1",
              "label": "San Diego 1"
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
            "{'$oid': '561d698b23d3fd6f1eb974b7'}",
            "{'$oid': '561d698b23d3fd6f1eb974b8'}",
            "{'$oid': '561d698b23d3fd6f1eb974b9'}"
          ],
          "validations": {},
          "field_id": "561d698b23d3fd6f1eb974b6",
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
            "group_id": "561d698b23d3fd6f1eb974b6"
          },
          "groups_fields": [],
          "required": true,
          "field_id": "561d698b23d3fd6f1eb974b7",
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
            "group_id": "561d698b23d3fd6f1eb974b6"
          },
          "groups_fields": [],
          "required": true,
          "field_id": "561d698b23d3fd6f1eb974b8",
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
            "group_id": "561d698b23d3fd6f1eb974b6"
          },
          "groups_fields": [],
          "required": true,
          "field_id": "561d698b23d3fd6f1eb974b9",
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
          "field_id": "561d698b23d3fd6f1eb974ba",
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
                    "value": 84
                  }
                ],
                "between": []
              },
              "send_alert": {
                "embed_company_picture": true,
                "sender": "OWNER_EMAIL",
                "send_pdf": true,
                "message": "El usuario {{record.user.name}} ha registrado una mortalidad de {{record.answers.55899c9401a4de2ea94629ea}} aves en la granja {{record.answers.55899c9401a4de2ea94629e8}} con fecha {{record.answers.55899c9401a4de2ea94629e7}}.\n\nEste aviso se genera cuando la mortalidad supera el 0.1%",
                "resend": "DONT_RESEND",
                "email": [
                  "amartin@sanfandila.com",
                  "jsolis@sanfandila.com",
                  "jjvega@sanfandila.com"
                ],
                "subject": "Mortalidad Alta en la granja {{record.answers.55899c9401a4de2ea94629e8}}."
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
      "field_id": "561d698b23d3fd6f1eb974b4",
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
      "field_id": "561d698b23d3fd6f1eb974b5",
      "label": "Granja",
      "visible": true,
      "options": [
        {
          "points": null,
          "selected": false,
          "value": "san_diego_1",
          "label": "San Diego 1"
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
          "$oid": "561d698b23d3fd6f1eb974b7"
        },
        {
          "$oid": "561d698b23d3fd6f1eb974b8"
        },
        {
          "$oid": "561d698b23d3fd6f1eb974b9"
        }
      ],
      "validations": {},
      "field_id": "561d698b23d3fd6f1eb974b6",
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
          "$oid": "561d698b23d3fd6f1eb974b6"
        }
      },
      "groups_fields": [],
      "required": true,
      "field_id": "561d698b23d3fd6f1eb974b7",
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
          "$oid": "561d698b23d3fd6f1eb974b6"
        }
      },
      "groups_fields": [],
      "required": true,
      "field_id": "561d698b23d3fd6f1eb974b8",
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
          "$oid": "561d698b23d3fd6f1eb974b6"
        }
      },
      "groups_fields": [],
      "required": true,
      "field_id": "561d698b23d3fd6f1eb974b9",
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
      "field_id": "561d698b23d3fd6f1eb974ba",
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
                "value": 84
              }
            ],
            "between": []
          },
          "send_alert": {
            "embed_company_picture": true,
            "sender": "OWNER_EMAIL",
            "send_pdf": true,
            "message": "El usuario {{record.user.name}} ha registrado una mortalidad de {{record.answers.55899c9401a4de2ea94629ea}} aves en la granja {{record.answers.55899c9401a4de2ea94629e8}} con fecha {{record.answers.55899c9401a4de2ea94629e7}}.\n\nEste aviso se genera cuando la mortalidad supera el 0.1%",
            "resend": "DONT_RESEND",
            "email": [
              "amartin@sanfandila.com",
              "jsolis@sanfandila.com",
              "jjvega@sanfandila.com"
            ],
            "subject": "Mortalidad Alta en la granja {{record.answers.55899c9401a4de2ea94629e8}}."
          }
        },
        "step": 1,
        "size": "small",
        "custom": null
      }
    }
  ],
  "created_at": 1444768139499,
  "private_url": "template-view/3398",
  "updated_at": 1444768152377,
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
  "resource_uri": "/api/infosync/form/3398/",
  "name": "Huevo - Mortalidad San Diego 1",
  "public": false,
  "description": ""
}