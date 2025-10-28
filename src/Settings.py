import settings


class StreetsOfRageSettings(settings.Group):
    class StreetsOfRageRomFile(settings.UserFilePath):
        """File name of the Streets of Rage ROM. Accepts (W) (REV 00) [!]"""
        required = True
        description = "Streets of Rage ROM File"
        copy_to = "Streets of Rage.md"
        md5s = [
            '569cfec15813294a8f0cf88cccc8c151' # (W) (REV 00) [!]
        ]

    rom_file: StreetsOfRageRomFile = StreetsOfRageRomFile(StreetsOfRageRomFile.copy_to)