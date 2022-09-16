#include <gst/gst.h>

#include <gst/rtsp-server/rtsp-server.h>

#include <sstream>
#include <fstream>

#define DEFAULT_RTSP_PORT "8554"

static char *port = (char *) DEFAULT_RTSP_PORT;

static GOptionEntry entries[] = {
        {"port", 'p', 0, G_OPTION_ARG_STRING, &port,
                "Port to listen on (default: " DEFAULT_RTSP_PORT ")", "PORT"},
        {nullptr}
};

int
main (int argc, char *argv[])
{
    GMainLoop *loop;
    GstRTSPServer *server;
    GstRTSPMountPoints *mounts;
    GstRTSPMediaFactory *factory;
    GOptionContext *optctx;
    GError *error = nullptr;

    optctx = g_option_context_new ("<launch line> - Cam RTSP Server, Launch\n\n"
                                   "Example: \" pipeline.conf\"");
    g_option_context_add_main_entries (optctx, entries, nullptr);
    g_option_context_add_group (optctx, gst_init_get_option_group ());
    if (!g_option_context_parse (optctx, &argc, &argv, &error)) {
        g_printerr ("Error parsing options: %s\n", error->message);
        g_option_context_free (optctx);
        g_clear_error (&error);
        return -1;
    }
    g_option_context_free (optctx);

    loop = g_main_loop_new (nullptr, FALSE);

    /* create a server instance */
    server = gst_rtsp_server_new ();
    g_object_set (server, "service", port, NULL);

    /* get the mount points for this server, every server has a default object
     * that be used to map uri mount points to media factories */
    mounts = gst_rtsp_server_get_mount_points (server);

    /* make a media factory for a test stream. The default media factory can use
     * gst-launch syntax to create pipelines.
     * any launch line works as long as it contains elements named pay%d. Each
     * element with pay%d names will be a stream */
    factory = gst_rtsp_media_factory_new ();

    std::ifstream t(argv[1]);
    std::stringstream buffer;
    buffer << t.rdbuf();
    auto pipeline = buffer.str();

    /* Set UDP */
    gst_rtsp_media_factory_set_protocols (factory, GST_RTSP_LOWER_TRANS_UDP);

    gst_rtsp_media_factory_set_launch (factory, pipeline.c_str());
    gst_rtsp_media_factory_set_shared (factory, TRUE);

    /* attach the test factory to the /test url */
    gst_rtsp_mount_points_add_factory (mounts, "/cam", factory);

    /* don't need the ref to the mapper anymore */
    g_object_unref (mounts);

    /* attach the server to the default maincontext */
    gst_rtsp_server_attach (server, nullptr);

    /* start serving */
    g_print ("stream ready at rtsp://127.0.0.1:%s/cam\n", port);
    g_main_loop_run (loop);

    return 0;
}
