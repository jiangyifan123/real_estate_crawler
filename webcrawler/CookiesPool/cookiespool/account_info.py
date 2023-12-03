accountInfo = {
    "zillow": {
        "serel33664@othao.com": "Nimbus_nova@123456",
        "pixime9052@othao.com": "Nimbus_nova@123456",
        "yajaref600@newnime.com": "Nimbus_nova@123456",
        "silovet502@mkurg.com": "Nimbus_nova@123456",
        "yivas90089@othao.com": "Nimbus_nova@123456",
        "sikod80761@cumzle.com": "Nimbus_nova@123456",
        "xahebe6049@dpsols.com": "Nimbus_nova@123456",
        "gaxabi3620@dpsols.com": "Nimbus_nova@123456",
        "cowaca2161@bustayes.com": "Nimbus_nova@123456",
        "hosetah600@cumzle.com": "Nimbus_nova@123456",
    },
    "realtor": {
        "serel33664@othao.com": "Nimbus_nova@123456",
        "pixime9052@othao.com": "Nimbus_nova@123456",
        "yajaref600@newnime.com": "Nimbus_nova@123456",
        "silovet502@mkurg.com": "Nimbus_nova@123456",
        "yivas90089@othao.com": "Nimbus_nova@123456",
        "sikod80761@cumzle.com": "Nimbus_nova@123456",
        "xahebe6049@dpsols.com": "Nimbus_nova@123456",
        "gaxabi3620@dpsols.com": "Nimbus_nova@123456",
        "cowaca2161@bustayes.com": "Nimbus_nova@123456",
        "hosetah600@cumzle.com": "Nimbus_nova@123456",
    }
}

def getAccountInfo(website=""):
    return accountInfo.get(website, {})