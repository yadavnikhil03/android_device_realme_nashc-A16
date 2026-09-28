#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/realme/nashc/device.mk)

# Inherit some common LineageOS stuff.
$(call inherit-product, vendor/pixelos/config/common_full_phone.mk)

PRODUCT_NAME := pixelos_nashc
PRODUCT_DEVICE := nashc
PRODUCT_MANUFACTURER := realme
PRODUCT_BRAND := Realme
PRODUCT_MODEL := RMX3085

PRODUCT_GMS_CLIENTID_BASE := android-realme

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildFingerprint=realme/RMX3085/RMX3085L1:13/SP1A.210812.016/R.1913398-178f6:user/release-keys \
    DeviceName=RMX3085L1 \
    DeviceProduct=RMX3085 \
    SystemDevice=RMX3085L1 \
    SystemName=RMX3085
