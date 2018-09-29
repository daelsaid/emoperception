{
  "name": "emoanger_model1",
  "description": "emo anger 1",
  "input": {
    "task": "emoperception"
  },
  "blocks": [
    {
      "level": "run",
      "transformations": [
        {
          "name": "factor",
          "input": [
            "trial_type"
          ]
        }
      ],
      "model": {
        "HRF_variables": [
          "trial_type.Finger",
          "trial_type.Foot",
          "trial_type.Lips"
        ],
        "variables": [
          "trial_type.Finger",
          "trial_type.Foot",
          "trial_type.Lips",
          "FramewiseDisplacement",
          "X",
          "Y",
          "Z",
          "RotX",
          "RotY",
          "RotZ",
          "aCompCor00",
          "aCompCor01",
          "aCompCor02",
          "aCompCor03",
          "aCompCor04",
          "aCompCor05"
        ]
      },
      "contrasts": [
        {
          "name": "finger_vs_others",
          "condition_list": [
            "trial_type.Finger",
            "trial_type.Foot",
            "trial_type.Lips"
          ],
          "weights": [
            1,
            -0.5,
            -0.5
          ],
          "type": "T"
        },
        {
          "name": "lips_vs_others",
          "condition_list": [
            "trial_type.Finger",
            "trial_type.Foot",
            "trial_type.Lips"
          ],
          "weights": [
            -0.5,
            -0.5,
            1
          ],
          "type": "T"
        }
      ]
    },
    {
      "level": "session",
      "transformations": [
        {
          "name": "split",
          "input": [
            "finger_vs_others"
          ],
          "by": "session"
        }
      ]
    },
    {
      "level": "subject",
      "model": {
        "variables": [
          "finger_vs_others.test",
          "finger_vs_others.retest"
        ]
      },
      "contrasts": [
        {
          "name": "session_diff",
          "condition_list": [
            "finger_vs_others.test",
            "finger_vs_others.retest"
          ],
          "weights": [
            1,
            -1
          ],
          "type": "T"
        }
      ]
    },
    {
      "level": "dataset",
      "model": {
        "variables": [
          "session_diff"
        ]
      },
      "contrasts": [
        {
          "name": "session_diff_finger_vs_others",
          "condition_list": [
            "session_diff"
          ],
          "weights": [
            1
          ],
          "type": "T"
        }
      ]
    }
  ]
}
