Sub RunUserInterface(args)
    ' boilerplate to display the full screen video player
    screen = CreateObject("roSGScreen")
    msgs = CreateObject("roMessagePort")
    screen.setMessagePort(msgs)
    scene = screen.CreateScene("playa")
    screen.show()

    ' setup to receieve messages via External Control API
    ' https://sdkdocs.roku.com/display/sdkdoc/External+Control+API#ExternalControlAPI-input
    input = CreateObject("roInput")
    input.SetMessagePort(msgs)

    while(true)
        msg = wait(0, msgs)
        msgType = type(msg)

        ' if they asked us to do something via the API do the needful
        if type(msg) = "roInputEvent"
            if msg.IsInput()
                info = msg.GetInfo()

                ' if the request contains a video key,
                ' then tell the player we have something
                if info.DoesExist("video") then
                    videocontent = createObject("RoSGNode", "ContentNode")
                    videocontent.title = info.video
                    videocontent.streamformat = "mp4"
                    videocontent.url = "ext1:/roku/"+info.video+".mp4"
                    scene.setField("content", videocontent)
                else
                    print "Unknown remote input: "; FormatJSON(info)
                end if
            end if
        end if

        ' this should never happen as our scene never closes, but in case
        ' there's a code path I don't know about, do the neednful
        if msgType = "roSGScreenEvent"
            if msg.isScreenClosed() then return
        end if
    end while
End Sub
