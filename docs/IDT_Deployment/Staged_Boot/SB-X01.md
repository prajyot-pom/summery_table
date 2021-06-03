# SB-X01
| Key                       | Value                                |
| -----------               | ------------------------------------ |
| Test-ID                   | SB-X01                               |
| Last-Tested               |                                      |
| Last-Tested-Image-Version |                                      |
| Status                    | Passed                               |
| Automated                 | No                                   |
| Designed-By               | Ravi                                 |
| Keywords                  |                                      |

## Description

``` mermaid
graph LR
  A[SRP] --> B{inital-state};
  B -->|shutdown| C{Staged-boot}
  C -->|Disabled| D[Don't check]
  C -->|Enabled| E[check]
  E -->|Next-subject| C
  D -->|Next-subject| C
```

## Dependencies

## Hardware-Requirements
[ ] Need one

## Steps

1. pre-setup-from-test-automation script 1
2. Step 2
3. step 3
4. post-setup-cleanup-from-test-automation

### Setup


## Comments
