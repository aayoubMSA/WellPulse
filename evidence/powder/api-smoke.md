# POWDER Portal API smoke — early-window probe

- Checked UTC: 2026-08-26T09:47:28Z
- WellPulse SHA: 7ece11ad31b647526b259dc0f3db8b47f7e93192
- Authentication gate: **PASS**
- Resource mutation attempted: **NONE**
- Exact `PowderProfiles/srslte-controlled-rf` matches in profile-list response: **0**
- Visible WellPulse experiments: **0**
- Reservation/resgroup API paths discovered: **5**
- Token content recorded: **NO**

## Experiment-create scheduling options

```text
│ *  --name                   TEXT                    A human readable name    │
│ *  --project                TEXT                    The project the          │
│ *  --profile-name           TEXT                    The name of the profile. │
│ *  --profile-project        TEXT                    The name of the profile  │
│                                                     project                  │
│    --group                  STR                     The project subgroup the │
│    --start-at               [%Y-%m-%dT%H:%M:%S%z|%  Schedule experiment to   │
│                             Y-%m-%dT%H:%M:%S.%f%z|  start at a future time   │
│    --stop-at                [%Y-%m-%dT%H:%M:%S%z|%  Schedule experiment to   │
│    --duration               INT                     Initial experiment       │
│                                                     duration in hours        │
│    --paramset-name          STR                     Optional name of a       │
│                                                     to the profile           │
│    --bindings               ANYOBJECT               [default: Unset]         │
│                                                     profile, optionally      │
```

## Root reservation-related CLI lines

```text
│ resgroup                                                                     │
```

## Reservation/resgroup OpenAPI operations

```json
{
  "/resgroups": {
    "get": {
      "body_schemas": [],
      "operationId": "listResgroups",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": "query",
          "name": "resgroup_id",
          "required": false
        },
        {
          "in": "query",
          "name": "creator",
          "required": false
        },
        {
          "in": "query",
          "name": "project",
          "required": false
        }
      ],
      "summary": null
    },
    "post": {
      "body_schemas": [
        {
          "properties": [],
          "ref": "#/components/schemas/ResGroup",
          "required": null
        }
      ],
      "operationId": "createResgroup",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": "query",
          "name": "duration",
          "required": false
        },
        {
          "in": "query",
          "name": "noautoapprove",
          "required": false
        }
      ],
      "summary": null
    }
  },
  "/resgroups/search": {
    "post": {
      "body_schemas": [
        {
          "properties": [],
          "ref": "#/components/schemas/ResGroupSearch",
          "required": null
        }
      ],
      "operationId": "searchResgroup",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": "query",
          "name": "duration",
          "required": true
        }
      ],
      "summary": null
    }
  },
  "/resgroups/{resgroup_id}": {
    "delete": {
      "body_schemas": [],
      "operationId": "deleteResgroup",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        }
      ],
      "summary": null
    },
    "get": {
      "body_schemas": [],
      "operationId": "getResgroup",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        }
      ],
      "summary": null
    },
    "put": {
      "body_schemas": [
        {
          "properties": [],
          "ref": "#/components/schemas/ResGroup",
          "required": null
        }
      ],
      "operationId": "ModifyResgroup",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": "query",
          "name": "duration",
          "required": false
        },
        {
          "in": "query",
          "name": "noautoapprove",
          "required": false
        }
      ],
      "summary": null
    }
  },
  "/resgroups/{resgroup_id}/reservations": {
    "post": {
      "body_schemas": [
        {
          "properties": [],
          "ref": "#/components/schemas/ResGroupReservation",
          "required": null
        }
      ],
      "operationId": "addResgroupReservation",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": "query",
          "name": "noautoapprove",
          "required": false
        }
      ],
      "summary": null
    }
  },
  "/resgroups/{resgroup_id}/reservations/{reservation_id}": {
    "delete": {
      "body_schemas": [],
      "operationId": "deleteResgroupReservation",
      "parameters": [
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        },
        {
          "in": null,
          "name": null,
          "required": false
        }
      ],
      "summary": null
    }
  }
}
```

## Reservation/resgroup schema fields

```json
{
  "ResGroup": {
    "properties": {
      "created_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "creator": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "expires_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "group": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      },
      "nodetypes": {
        "format": null,
        "ref": "#/components/schemas/ResGroupNodeTypes",
        "type": null
      },
      "powder_zones": {
        "format": null,
        "ref": "#/components/schemas/PowderZones",
        "type": null
      },
      "project": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "ranges": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRanges",
        "type": null
      },
      "reason": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "routes": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRoutes",
        "type": null
      },
      "start_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      }
    },
    "required": [
      "project",
      "reason"
    ]
  },
  "ResGroupError": {
    "properties": {
      "error": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "errorCode": {
        "format": null,
        "ref": null,
        "type": "integer"
      },
      "nodetypes": {
        "format": null,
        "ref": "#/components/schemas/ResGroupNodeTypes",
        "type": null
      },
      "ranges": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRanges",
        "type": null
      },
      "routes": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRoutes",
        "type": null
      }
    },
    "required": []
  },
  "ResGroupList": {
    "properties": {
      "resgroups": {
        "format": null,
        "ref": null,
        "type": "array"
      }
    },
    "required": []
  },
  "ResGroupNodeType": {
    "properties": {
      "approved_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "canceled_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "count": {
        "format": null,
        "ref": null,
        "type": "integer"
      },
      "deleted_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "error": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "errorCode": {
        "format": null,
        "ref": null,
        "type": "integer"
      },
      "nodetype": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "reservation_id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      },
      "resgroup_id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      },
      "urn": {
        "format": null,
        "ref": null,
        "type": "string"
      }
    },
    "required": [
      "nodetype",
      "count",
      "urn"
    ]
  },
  "ResGroupNodeTypes": {
    "properties": {
      "nodetypes": {
        "format": null,
        "ref": null,
        "type": "array"
      }
    },
    "required": []
  },
  "ResGroupRange": {
    "properties": {
      "approved_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "canceled_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "error": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "errorCode": {
        "format": null,
        "ref": null,
        "type": "integer"
      },
      "max_freq": {
        "format": "float",
        "ref": null,
        "type": "number"
      },
      "min_freq": {
        "format": "float",
        "ref": null,
        "type": "number"
      },
      "reservation_id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      },
      "resgroup_id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      }
    },
    "required": [
      "min_freq",
      "max_freq"
    ]
  },
  "ResGroupRanges": {
    "properties": {
      "ranges": {
        "format": null,
        "ref": null,
        "type": "array"
      }
    },
    "required": []
  },
  "ResGroupReservation": {
    "properties": {
      "nodetype": {
        "format": null,
        "ref": "#/components/schemas/ResGroupNodeType",
        "type": null
      },
      "range": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRange",
        "type": null
      },
      "route": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRoute",
        "type": null
      }
    },
    "required": []
  },
  "ResGroupRoute": {
    "properties": {
      "approved_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "canceled_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "name": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "reservation_id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      },
      "resgroup_id": {
        "format": "uuid",
        "ref": null,
        "type": "string"
      }
    },
    "required": [
      "name"
    ]
  },
  "ResGroupRoutes": {
    "properties": {
      "routes": {
        "format": null,
        "ref": null,
        "type": "array"
      }
    },
    "required": []
  },
  "ResGroupSearch": {
    "properties": {
      "group": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "nodetypes": {
        "format": null,
        "ref": "#/components/schemas/ResGroupNodeTypes",
        "type": null
      },
      "project": {
        "format": null,
        "ref": null,
        "type": "string"
      },
      "ranges": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRanges",
        "type": null
      },
      "routes": {
        "format": null,
        "ref": "#/components/schemas/ResGroupRoutes",
        "type": null
      }
    },
    "required": [
      "project"
    ]
  },
  "ResGroupSearchResult": {
    "properties": {
      "expires_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      },
      "start_at": {
        "format": "date-time",
        "ref": null,
        "type": "string"
      }
    },
    "required": []
  }
}
```
