import settings


class StreetsOfRageSettings(settings.Group):
    class StreetsOfRageRomFile(settings.UserFilePath):
        """File name of the Streets of Rage ROM. Accepts (W) (REV 00) [!], 3DS, Steam"""
        required = True
        description = "Streets of Rage ROM File"
        copy_to = "Streets of Rage.md"
        md5s = [
            '0de64a4f7dd5b0f11fbeea8c2c83f253', # 3DS UE
            '569cfec15813294a8f0cf88cccc8c151', # (W) (REV 00) [!]
            '59a3b22a1899461dceba50d1ade88d3a', # Steam
        ]

    rom_file: StreetsOfRageRomFile = StreetsOfRageRomFile(StreetsOfRageRomFile.copy_to)