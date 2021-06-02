# IDT-PROV-02
| Key                       | Value                                |
| -----------               | ------------------------------------ |
| Test-ID                   | IDT-PROV-02                          |
| Last-Tested               |                                      |
| Last-Tested-Image-Version |                                      |
| Status                    |                                      |
| Automated                 |                                      |
| Designed-By               |                                      |
| Keywords                  |                                      |

## Test Description

Verify that a new SRP can be copied by unlocking a locked disk

## Dependencies

## Hardware-Requirements

[ ] Need one

## Setup

## Pre-Conditions

## Test Steps

(linuxpba --passphrase <password>
blockdev --rereadpt /dev/nvme0n1
mount /dev/disk/by-partlabel/lsk /mnt
cp srp.elf /mnt
sync
umount /mnt)

## Expected Outcome

## Comments